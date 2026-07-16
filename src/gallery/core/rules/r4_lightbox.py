"""Rule R4: Interactive Lightbox View."""

from typing import Optional
from gallery.core.models import Request, Decision
from gallery.core.rules.base import Rule
from gallery.core.rules.r1_default_photos import R1DefaultPhotos


class R4Lightbox(Rule):
    """Rule that returns high-resolution metadata for a clicked photo

    to open in a Lightbox overlay.
    """


    def __init__(self) -> None:
        self.r1_rule = R1DefaultPhotos()

    def evaluate(self, request: Request) -> Optional[Decision]:
        """Loads and returns details of the clicked photo if matching.

        Args:
            request: The evaluation request containing photo_id.

        Returns:
            A Decision with OPEN_LIGHTBOX outcome containing the clicked photo in photos,
            or None if conditions are not met.
        """
        if request.event == "click_photo" and request.photo_id is not None:
            # Look up the clicked photo in the master photo collection
            for photo in self.r1_rule.default_photos:
                if photo.id == request.photo_id:
                    return Decision(
                        outcome="OPEN_LIGHTBOX",
                        photos=[photo],
                        rule_ids=["R4"],
                    )
        return None
