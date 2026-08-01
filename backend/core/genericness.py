"""
genericness.py

Deterministic genericness penalty calculation.

The AI (see prompts/content_evaluation_prompt.py, once implemented)
only *detects* generic-language signals — clichés, vague claims,
interchangeable phrases — as raw structured data
(models.evaluation.GenericnessSignals). Per Principle 1 in the
developer handbook, it never outputs the penalty number itself; this
module converts those raw signals into the numeric deduction applied
to the final score.
"""

from config import settings
from models.evaluation import GenericnessSignals

# Fixed by 02_bdsf.yaml `genericness_penalty.maximum_deduction`. This
# is part of the frozen BDSF framework, not a tunable implementation
# threshold, so it is a constant rather than a config setting.
# NOTE: 08_api_contracts.md's Validation Rules table separately lists
# "Genericness Penalty: 0–20", which conflicts with this 10-point cap
# from the dedicated BDSF framework doc. 02_bdsf.yaml is treated as
# authoritative here since it defines the actual scoring formula;
# flagged for the next spec-consistency audit.
_MAX_DEDUCTION = 10


def calculate_genericness_penalty(signals: GenericnessSignals) -> int:
    """
    Converts raw genericness signals into a point deduction.

    Each detected indicator (regardless of which of the three
    categories it falls into — 02_bdsf.yaml does not weight them
    differently) costs `settings.genericness_points_per_indicator`
    points, capped at the framework's maximum deduction.
    """
    total_indicators = (
        len(signals.cliches)
        + len(signals.vague_claims)
        + len(signals.interchangeable_phrases)
    )
    penalty = total_indicators * settings.genericness_points_per_indicator
    return int(min(_MAX_DEDUCTION, round(penalty)))
