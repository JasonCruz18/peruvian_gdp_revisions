"""Progress bar utilities for Peru GDP RTD pipeline."""

from typing import Iterable, Optional

from tqdm import tqdm

PROGRESS_BAR_COLOR = "#3366FF"


def progress_bar(
    iterable: Iterable,
    desc: str,
    unit: Optional[str] = None,
    total: Optional[int] = None,
    disable: bool = False,
) -> tqdm:
    """Create a tqdm progress bar with the project-standard style."""
    return tqdm(
        iterable,
        desc=desc,
        unit=unit,
        total=total,
        colour=PROGRESS_BAR_COLOR,
        disable=disable,
    )
