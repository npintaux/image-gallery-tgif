"""Unit tests for R1: Served Default Photos on Load."""

from gallery.core.models import Request, Photo
from gallery.core.rules.r1_default_photos import R1DefaultPhotos


def test_r1_applies_on_load_gallery():
    """R1 should apply on the 'load_gallery' event and return 6 default photos."""
    request = Request(event="load_gallery", viewport_width=1200)
    rule = R1DefaultPhotos()

    decision = rule.evaluate(request)

    assert decision is not None
    assert decision.outcome == "SERVE_PHOTOS"
    assert decision.rule_ids == ["R1"]
    assert len(decision.photos) == 6

    # Verify each photo satisfies metadata completeness
    for idx, photo in enumerate(decision.photos, 1):
        assert isinstance(photo, Photo)
        assert photo.id == f"photo_{idx}"
        assert photo.title != ""
        assert photo.category in ["Nature", "Urban", "Minimal"]
        assert photo.image_url != ""
        assert photo.likes == 0


def test_r1_does_not_apply_on_other_events():
    """R1 should return None on events other than 'load_gallery'."""
    request = Request(event="hover_photo", photo_id="photo_1", viewport_width=1200)
    rule = R1DefaultPhotos()

    decision = rule.evaluate(request)

    assert decision is None
