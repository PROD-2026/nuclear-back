from dataclasses import dataclass


@dataclass(frozen=True)
class SeverityInfo:
    critical: int
    high: int
    medium: int
    low: int

    def __post_init__(self) -> None:
        if self.critical < 0 or self.high < 0 or self.medium < 0 or self.low < 0:
            raise ValueError("Counts must be greater than or equals 0")
