"""Base schemas for AGoT."""

from typing import TypedDict

type Thought = str
type Answer = str
type Strategy = str
type Edge = tuple[str, str]  # (идентификатор_родитель, идентификатор_потомка)
type Heritage = list[tuple[int, int]]


class AGoTParams(TypedDict):
    lmax: int
    nmax: int
    max_depth: int
