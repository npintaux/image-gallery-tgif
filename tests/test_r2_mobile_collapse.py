"""Unit tests for R2: Mobile Grid Collapse."""

from gallery.core.models import Request
from gallery.core.rules.r2_mobile_collapse import R2MobileCollapse


def test_r2_applies_on_mobile_viewports():
    """R2 should apply on load_gallery with viewport_width < 768."""
    request = Request(event="load_gallery", viewport_width=375)
    rule = R2MobileCollapse()

    decision = rule.evaluate(request)

    assert decision is not None
    assert decision.outcome == "SERVE_PHOTOS"
    assert decision.rule_ids == ["R1", "R2"]
    assert len(decision.photos) == 6


def test_r2_does_not_apply_on_desktop_viewports():
    """R2 should return None on viewports >= 768."""
    rule = R2MobileCollapse()

    # Exact boundary (768px)
    assert rule.evaluate(Request(event="load_gallery", viewport_width=768)) is None

    # Desktop (1200px)
    assert rule.evaluate(Request(event="load_gallery", viewport_width=1200)) is None


def test_r2_does_not_apply_on_other_events():
    """R2 should return None on events other than 'load_gallery'."""
    request = Request(event="hover_photo", photo_id="photo_1", viewport_width=375)
    rule = R2MobileCollapse()

    assert rule.evaluate(request) is None
