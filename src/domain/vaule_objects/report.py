from dataclasses import dataclass

from litestar.datastructures import UploadFile


@dataclass(frozen=True)
class ReportIn:
    file: UploadFile
    blacklist: list[str] | None = None
    whitelist: list[str] | None = None

    def __post_init__(self) -> None:
        print(self.blacklist, self.whitelist)
        if self.blacklist and self.whitelist:
            raise ValueError(
                "Blacklist and whitelist cannot be provided at the same time"
            )
