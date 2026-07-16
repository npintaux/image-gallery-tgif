"""Smart Photo Gallery execution engine."""

from gallery.core.models import Request, Decision
from gallery.core.rules.r1_default_photos import R1DefaultPhotos

# Active rules list, ordered by precedence
RULES = [
    R1DefaultPhotos(),
]


def evaluate(request: Request) -> Decision:
    """Evaluates the input request against all registered rules in precedence order.

    Args:
        request: The input request parameters.

    Returns:
        The first valid Decision output from an active rule.

    Raises:
        ValueError: If no active rules apply to the request.
    """
    for rule in RULES:
        decision = rule.evaluate(request)
        if decision is not None:
            return decision

    raise ValueError("No rules applied to the request")
