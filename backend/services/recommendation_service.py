from models.evaluation import (
    ContentEvaluationResult,
    Recommendations,
)


def generate_recommendations(
    evaluation_result: ContentEvaluationResult,
) -> Recommendations:
    quick_fixes = []
    strategic_improvements = []

    # Identity
    if evaluation_result.identity.score < 70:
        quick_fixes.append(
            "Strengthen references to the brand's mission, positioning, and unique identity."
        )

    # Personality
    if evaluation_result.personality.score < 70:
        quick_fixes.append(
            "Use language that better reflects the brand's personality traits and emotional style."
        )

    # Communication
    if evaluation_result.communication.score < 70:
        quick_fixes.append(
            "Incorporate more preferred brand vocabulary and messaging pillars."
        )

    # Audience
    if evaluation_result.audience.score < 70:
        quick_fixes.append(
            "Address the needs and interests of the target audience more directly."
        )

    # Visual Identity
    if evaluation_result.visual_identity.score < 70:
        quick_fixes.append(
            "Include references to the brand's visual identity, imagery, or design style."
        )

    # Values
    if evaluation_result.values.score < 70:
        quick_fixes.append(
            "Highlight the brand's core values and promises more clearly."
        )

    # Strategic Improvements
    if evaluation_result.communication.score < 80:
        strategic_improvements.append(
            "Build stronger consistency across messaging pillars and tone of voice."
        )

    if evaluation_result.identity.score < 80:
        strategic_improvements.append(
            "Differentiate the content using more brand-specific positioning and differentiators."
        )

    if evaluation_result.audience.score < 80:
        strategic_improvements.append(
            "Create audience-specific variations for different customer segments."
        )

    if evaluation_result.visual_identity.score < 80:
        strategic_improvements.append(
            "Align future content with the brand's visual storytelling guidelines."
        )

    return Recommendations(
        quick_fixes=quick_fixes,
        strategic_improvements=strategic_improvements,
    )
