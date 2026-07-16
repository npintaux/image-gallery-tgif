"""Engine-level integration tests."""

import pytest
from gallery.core.models import Request
from gallery.core.engine import evaluate


def test_engine_evaluates_load_gallery_through_r1():
    """The engine should process a 'load_gallery' request using R1."""
    request = Request(event="load_gallery", viewport_width=1200)

    decision = evaluate(request)

    assert decision.outcome == "SERVE_PHOTOS"
    assert decision.rule_ids == ["R1"]
    assert len(decision.photos) == 6


def test_engine_evaluates_load_gallery_through_r2_on_mobile():
    """The engine should evaluate load_gallery on mobile through R2."""
    request = Request(event="load_gallery", viewport_width=375)

    decision = evaluate(request)

    assert decision.outcome == "SERVE_PHOTOS"
    assert decision.rule_ids == ["R1", "R2"]
    assert len(decision.photos) == 6


def test_engine_evaluates_hover_photo_through_r3():
    """The engine should process a 'hover_photo' request using R3."""
    request = Request(event="hover_photo", photo_id="photo_1", viewport_width=1200)

    decision = evaluate(request)

    assert decision.outcome == "ZOOM_PHOTO"
    assert decision.rule_ids == ["R3"]
    assert len(decision.photos) == 0


def test_engine_evaluates_click_photo_through_r4():
    """The engine should process a 'click_photo' request using R4."""
    request = Request(event="click_photo", photo_id="photo_1", viewport_width=1200)

    decision = evaluate(request)

    assert decision.outcome == "OPEN_LIGHTBOX"
    assert decision.rule_ids == ["R4"]
    assert len(decision.photos) == 1
    assert decision.photos[0].id == "photo_1"


def test_engine_evaluates_load_gallery_through_r5_with_category():
    """The engine should process a 'load_gallery' request with a specific category using R5."""
    request = Request(event="load_gallery", category="Urban", viewport_width=1200)

    decision = evaluate(request)

    assert decision.outcome == "SERVE_PHOTOS"
    assert decision.rule_ids == ["R1", "R5"]
    assert len(decision.photos) > 0
    assert all(photo.category == "Urban" for photo in decision.photos)


def test_engine_raises_error_when_no_rules_apply():
    """The engine should raise a ValueError when no rules apply to the request."""
    request = Request(event="unknown_event", viewport_width=1200)

    with pytest.raises(ValueError, match="No rules applied to the request"):
        evaluate(request)
