"""Rule R2: Mobile Grid Collapse."""

from typing import Optional
from gallery.core.models import Request, Decision
from gallery.core.rules.base import Rule
from gallery.core.rules.r1_default_photos import R1DefaultPhotos


class R2MobileCollapse(Rule):
    """Rule that collapses the photo grid to a single-column layout on mobile viewports."""

    def __init__(self) -> None:
        self.r1_rule = R1DefaultPhotos()

    def evaluate(self, request: Request) -> Optional[Decision]:
        """Triggers mobile layout instructions if the viewport width is under 768px.

        Args:
            request: The evaluation request.

        Returns:
            A Decision with the default photos and both R1 and R2 in rule_ids,
            or None if the viewport width is 768px or greater.
        """
        if request.event == "load_gallery" and request.viewport_width < 768:
            return Decision(
                outcome="SERVE_PHOTOS",
                photos=self.r1_rule.default_photos,
                rule_ids=["R1", "R2"],
            )
        return None
