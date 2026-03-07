from dataclasses import dataclass


@dataclass(frozen=True)
class Pagination[IT]:
    items: list[IT]
    total: int
