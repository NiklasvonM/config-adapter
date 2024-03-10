from __future__ import annotations

from abc import ABC, abstractmethod


class LoaderStrategy(ABC):
    @abstractmethod
    def load(self) -> dict:
        pass
