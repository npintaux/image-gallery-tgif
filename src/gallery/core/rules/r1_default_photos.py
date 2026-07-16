"""Rule R1: Served Default Photos on Load."""

from typing import Optional
from gallery.core.models import Request, Decision, Photo
from gallery.core.rules.base import Rule


class R1DefaultPhotos(Rule):
    """Rule that serves exactly 6 default photos upon gallery initialization."""

    def __init__(self) -> None:
        self.default_photos = [
            Photo(
                id="photo_1",
                title="Golden Hour Reflections",
                category="Nature",
                image_url="/assets/images/golden-hour.jpg",
                likes=0,
            ),
            Photo(
                id="photo_2",
                title="Urban Neon Pulse",
                category="Urban",
                image_url="/assets/images/urban-neon.jpg",
                likes=0,
            ),
            Photo(
                id="photo_3",
                title="Minimalist Shadows",
                category="Minimal",
                image_url="/assets/images/minimalist-shadows.jpg",
                likes=0,
            ),
            Photo(
                id="photo_4",
                title="Mist in the Pine Forest",
                category="Nature",
                image_url="/assets/images/pine-forest.jpg",
                likes=0,
            ),
            Photo(
                id="photo_5",
                title="Brutalist Concrete Angles",
                category="Urban",
                image_url="/assets/images/brutalist-concrete.jpg",
                likes=0,
            ),
            Photo(
                id="photo_6",
                title="Abstract Curved Lines",
                category="Minimal",
                image_url="/assets/images/abstract-curves.jpg",
                likes=0,
            ),
        ]

    def evaluate(self, request: Request) -> Optional[Decision]:
        """Serves default photos if the request is for loading the gallery.

        Args:
            request: The evaluation request.

        Returns:
            A Decision containing the default photos if evaluated, else None.
        """
        if request.event == "load_gallery":
            return Decision(
                outcome="SERVE_PHOTOS",
                photos=self.default_photos,
                rule_ids=["R1"],
            )
        return None
