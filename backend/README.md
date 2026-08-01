# BrandDistinct AI — Backend

## Setup

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then fill in GEMINI_API_KEY
```

## Run

```bash
uvicorn main:app --reload
```

- Docs: http://localhost:8000/docs
- Health check: http://localhost:8000/api/health

## Status

Foundation only. Brand Discovery and Evaluation engines are not yet
implemented (see 07_developer_handbook.md and 03_evaluation_pipeline.yaml
for the planned architecture).
