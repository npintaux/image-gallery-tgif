"""Core models and data structures for the gallery engine."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass(frozen=True)
class Photo:
    """Represents a photo's metadata and state."""

    id: str
    title: str
    category: str
    image_url: str
    likes: int = 0


@dataclass(frozen=True)
class Request:
    """Represents a request to evaluate gallery operations."""

    event: str
    viewport_width: int
    photo_id: Optional[str] = None
    category: Optional[str] = None



@dataclass(frozen=True)
class Decision:
    """Represents the output decision of a request evaluation."""

    outcome: str
    photos: list[Photo] = field(default_factory=list)
    rule_ids: list[str] = field(default_factory=list)
    evaluated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
