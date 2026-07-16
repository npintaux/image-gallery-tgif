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


def test_engine_raises_error_when_no_rules_apply():
    """The engine should raise a ValueError when no rules apply to the request."""
    request = Request(event="unknown_event", viewport_width=1200)

    with pytest.raises(ValueError, match="No rules applied to the request"):
        evaluate(request)
