from __future__ import annotations

from pathlib import Path
from typing import Any

Readable = str | Path
Convertable = dict[str, Any]  # TODO: Add support for lists
Input = Convertable | Readable
