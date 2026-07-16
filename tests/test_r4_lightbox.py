"""Unit tests for R4: Interactive Lightbox View."""

from gallery.core.models import Request
from gallery.core.rules.r4_lightbox import R4Lightbox


def test_r4_applies_on_click_photo():
    """R4 should apply on click_photo event with a valid photo_id."""
    request = Request(event="click_photo", photo_id="photo_1", viewport_width=1200)
    rule = R4Lightbox()

    decision = rule.evaluate(request)

    assert decision is not None
    assert decision.outcome == "OPEN_LIGHTBOX"
    assert decision.rule_ids == ["R4"]
    assert len(decision.photos) == 1
    assert decision.photos[0].id == "photo_1"


def test_r4_does_not_apply_without_photo_id():
    """R4 should return None if photo_id is missing on click_photo."""
    request = Request(event="click_photo", photo_id=None, viewport_width=1200)
    rule = R4Lightbox()

    assert rule.evaluate(request) is None


def test_r4_does_not_apply_with_invalid_photo_id():
    """R4 should return None if photo_id does not exist in the collection."""
    request = Request(event="click_photo", photo_id="invalid_id", viewport_width=1200)
    rule = R4Lightbox()

    assert rule.evaluate(request) is None


def test_r4_does_not_apply_on_other_events():
    """R4 should return None on events other than 'click_photo'."""
    request = Request(event="load_gallery", viewport_width=1200)
    rule = R4Lightbox()

    assert rule.evaluate(request) is None
