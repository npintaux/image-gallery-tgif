"""Abstract Base Class for evaluation rules."""

from abc import ABC, abstractmethod
from typing import Optional
from gallery.core.models import Request, Decision


class Rule(ABC):
    """Abstract base class representing a single evaluation rule."""

    @abstractmethod
    def evaluate(self, request: Request) -> Optional[Decision]:
        """Evaluates the request and returns a Decision, or None if the rule does not apply.

        Args:
            request: The input request parameters.

        Returns:
            A Decision if the rule fires, else None.
        """
