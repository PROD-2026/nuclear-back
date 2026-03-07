from dataclasses import dataclass


@dataclass(frozen=True)
class Recommendations:
    text: str
