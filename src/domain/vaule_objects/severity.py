from dataclasses import dataclass


@dataclass(frozen=True)
class SeverityInfo:
    critical: int = 0
    high: int = 0
    medium: int = 0
    low: int = 0

    def __post_init__(self) -> None:
        if self.critical < 0 or self.high < 0 or self.medium < 0 or self.low < 0:
            raise ValueError("Counts must be greater than or equals 0")
