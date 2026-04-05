"""Compatibility shim for the old philosophy-oriented module path."""

from .transcript_refinement import (
    BPPhilosophySystem,
    OptimizedBPPhilosophySystem,
    TranscriptRefinementSystem,
)

__all__ = [
    "BPPhilosophySystem",
    "OptimizedBPPhilosophySystem",
    "TranscriptRefinementSystem",
]
