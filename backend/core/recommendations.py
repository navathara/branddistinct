from models.evaluation import Recommendations


def generate_recommendations(evaluation_result):
    quick_fixes = []
    strategic_improvements = []

    if evaluation_result.communication.score < 70:
        quick_fixes.append(
            "Use more brand-preferred vocabulary and messaging pillars."
        )

    if evaluation_result.visual_identity.score < 70:
        quick_fixes.append(
            "Include references to the brand's visual identity."
        )

    if evaluation_result.personality.score < 70:
        strategic_improvements.append(
            "Reflect the brand personality more consistently."
        )

    if evaluation_result.audience.score < 70:
        strategic_improvements.append(
            "Address additional target audience segments."
        )

    if evaluation_result.values.score < 70:
        strategic_improvements.append(
            "Highlight core brand values more explicitly."
        )

    return Recommendations(
        quick_fixes=quick_fixes,
        strategic_improvements=strategic_improvements,
    )
