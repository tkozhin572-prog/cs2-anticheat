from .accuracy import HeadshotRatioDetector, RecoilConsistencyDetector
from .aim import CrosshairPlacementDetector, SnapAimDetector
from .movement import MovingAccuracyDetector
from .reaction import FastReactionDetector, ReactionConsistencyDetector

DEFAULT_DETECTORS = (
    FastReactionDetector(),
    ReactionConsistencyDetector(),
    SnapAimDetector(),
    CrosshairPlacementDetector(),
    HeadshotRatioDetector(),
    RecoilConsistencyDetector(),
    MovingAccuracyDetector(),
)

__all__ = ["DEFAULT_DETECTORS"]
