"""
main.py

Application entry point.

Responsible for:
- Building the FastAPI app instance (via an app factory)
- Registering middleware (CORS)
- Mounting the aggregated API router under the configured prefix
- Defining startup/shutdown lifecycle behavior

This file must stay thin. It contains no business logic, no
evaluation logic, and no direct AI calls — those live in
core/, services/, and api/routes/ respectively.

Run locally with:
    uvicorn main:app --reload
"""

from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import settings
from api.router import api_router
from core.exceptions import BrandDiscoveryError
from models.response import ErrorDetail, ErrorResponse

logger = logging.getLogger(__name__)


async def _domain_error_handler(request: Request, exc: BrandDiscoveryError) -> JSONResponse:
    """
    Translates any domain exception into the standard ErrorResponse.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=ErrorDetail(code=exc.code, message=exc.message)
        ).model_dump(),
    )


async def _validation_error_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Malformed request bodies -> INVALID_REQUEST."""
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            error=ErrorDetail(
                code="INVALID_REQUEST",
                message="Request validation failed.",
            )
        ).model_dump(),
    )


async def _unhandled_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """Last-resort catch-all."""
    logger.exception("Unhandled exception occurred.")

    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error=ErrorDetail(
                code="INTERNAL_ERROR",
                message="An unexpected error occurred.",
            )
        ).model_dump(),
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    logger.info(
        "%s v%s starting in '%s' mode",
        settings.app_name,
        settings.app_version,
        settings.environment,
    )

    logger.info("Claude model: %s", settings.claude_model)
    logger.info("Allowed origins: %s", settings.allowed_origins)

    yield

    # --- Shutdown ---
    logger.info("%s shutting down", settings.app_name)


def create_app() -> FastAPI:
    """
    Application factory.
    """

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.api_prefix)

    app.add_exception_handler(BrandDiscoveryError, _domain_error_handler)
    app.add_exception_handler(RequestValidationError, _validation_error_handler)
    app.add_exception_handler(Exception, _unhandled_exception_handler)

    return app


app = create_app()
