"""Rule R5: Dynamic Category Filters."""

from typing import Optional
from gallery.core.models import Request, Decision
from gallery.core.rules.base import Rule
from gallery.core.rules.r1_default_photos import R1DefaultPhotos


class R5Filters(Rule):
    """Rule that filters the served photos list to match a requested category."""

    def __init__(self) -> None:
        self.r1_rule = R1DefaultPhotos()

    def evaluate(self, request: Request) -> Optional[Decision]:
        """Filters the default photos collection if a specific category is requested.

        Args:
            request: The evaluation request.

        Returns:
            A Decision with the filtered photos collection, or None if category
            is missing or "All".
        """
        if (
            request.event == "load_gallery"
            and request.category is not None
            and request.category.lower() != "all"
        ):
            # Filter the default photo collection by category case-insensitively
            filtered = [
                photo
                for photo in self.r1_rule.default_photos
                if photo.category.lower() == request.category.lower()
            ]

            # Accumulate rules: R1 is the source of photos, R5 is the filter
            rule_ids = ["R1", "R5"]
            if request.viewport_width < 768:
                # Accumulate R2 if evaluating on a mobile viewport size
                rule_ids = ["R1", "R2", "R5"]

            return Decision(
                outcome="SERVE_PHOTOS",
                photos=filtered,
                rule_ids=rule_ids,
            )

        return None
