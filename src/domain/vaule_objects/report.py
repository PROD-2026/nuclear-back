from dataclasses import dataclass

from litestar.datastructures import UploadFile


@dataclass(frozen=True)
class ReportIn:
    file: UploadFile
    blacklist: list[str] | None = None
    whitelist: list[str] | None = None
