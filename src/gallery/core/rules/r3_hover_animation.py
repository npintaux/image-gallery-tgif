"""Rule R3: Smooth Hover Micro-Animation."""

from typing import Optional
from gallery.core.models import Request, Decision
from gallery.core.rules.base import Rule


class R3HoverAnimation(Rule):
    """Rule that triggers a zoom effect outcome when a photo card is hovered."""

    def evaluate(self, request: Request) -> Optional[Decision]:
        """Triggers a ZOOM_PHOTO outcome on hover_photo events if a photo_id is present.

        Args:
            request: The evaluation request.

        Returns:
            A Decision with ZOOM_PHOTO outcome if evaluated, else None.
        """
        if request.event == "hover_photo" and request.photo_id is not None:
            return Decision(
                outcome="ZOOM_PHOTO",
                rule_ids=["R3"],
            )
        return None
