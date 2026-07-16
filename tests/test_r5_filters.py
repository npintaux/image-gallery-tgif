"""Unit tests for R5: Dynamic Category Filters."""

from gallery.core.models import Request
from gallery.core.rules.r5_filters import R5Filters


def test_r5_filters_photos_by_category():
    """R5 should apply on load_gallery with a specific category."""
    request = Request(event="load_gallery", category="Nature", viewport_width=1200)
    rule = R5Filters()

    decision = rule.evaluate(request)

    assert decision is not None
    assert decision.outcome == "SERVE_PHOTOS"
    assert decision.rule_ids == ["R1", "R5"]
    assert len(decision.photos) > 0
    assert all(photo.category == "Nature" for photo in decision.photos)


def test_r5_does_not_filter_on_all_category():
    """R5 should return None (not apply) when category is 'All'."""
    request = Request(event="load_gallery", category="All", viewport_width=1200)
    rule = R5Filters()

    assert rule.evaluate(request) is None


def test_r5_does_not_filter_on_missing_category():
    """R5 should return None (not apply) when category is None."""
    request = Request(event="load_gallery", category=None, viewport_width=1200)
    rule = R5Filters()

    assert rule.evaluate(request) is None


def test_r5_does_not_apply_on_other_events():
    """R5 should return None on events other than 'load_gallery'."""
    request = Request(event="hover_photo", category="Nature", viewport_width=1200)
    rule = R5Filters()

    assert rule.evaluate(request) is None


def test_r5_applies_on_mobile_and_accumulates_r2():
    """R5 should apply on load_gallery with a category on mobile, adding R2 to rule_ids."""
    request = Request(event="load_gallery", category="Nature", viewport_width=375)
    rule = R5Filters()

    decision = rule.evaluate(request)

    assert decision is not None
    assert decision.outcome == "SERVE_PHOTOS"
    assert decision.rule_ids == ["R1", "R2", "R5"]
    assert all(photo.category == "Nature" for photo in decision.photos)
