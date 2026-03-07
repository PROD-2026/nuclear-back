from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from uuid import uuid4

from src.domain.vaule_objects.severity import SeverityInfo
from src.domain.vaule_objects.vulnerability import (
    FileVulnerabilities,
    Vulnerability,
)


class ReportStatus(StrEnum):
    PENDING = "pending"
    PREPARING = "preparing"
    SCANNING = "scanning"
    ML_ANALYZING = "ml_analyzing"
    GENERATING_RECOMENDATIONS = "generating_recomendations"
    DONE = "done"


@dataclass
class Report:
    status: ReportStatus = ReportStatus.PENDING
    vulnerabilities_count: int = 0
    vulnerabilities: list[Vulnerability] | None = None
    files_with_most_vulnerabilities: list[FileVulnerabilities] | None = None
    severity_distribution: SeverityInfo | None = None
    id: str = field(default_factory=lambda: str(uuid4()))

    created_at: datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))
