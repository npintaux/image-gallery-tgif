"""Unit tests for R3: Smooth Hover Micro-Animation."""

from gallery.core.models import Request
from gallery.core.rules.r3_hover_animation import R3HoverAnimation


def test_r3_applies_on_hover_photo():
    """R3 should apply on hover_photo event with a valid photo_id."""
    request = Request(event="hover_photo", photo_id="photo_1", viewport_width=1200)
    rule = R3HoverAnimation()

    decision = rule.evaluate(request)

    assert decision is not None
    assert decision.outcome == "ZOOM_PHOTO"
    assert decision.rule_ids == ["R3"]
    assert len(decision.photos) == 0


def test_r3_does_not_apply_without_photo_id():
    """R3 should return None if photo_id is missing on hover_photo."""
    request = Request(event="hover_photo", photo_id=None, viewport_width=1200)
    rule = R3HoverAnimation()

    assert rule.evaluate(request) is None


def test_r3_does_not_apply_on_other_events():
    """R3 should return None on events other than 'hover_photo'."""
    request = Request(event="load_gallery", viewport_width=1200)
    rule = R3HoverAnimation()

    assert rule.evaluate(request) is None
