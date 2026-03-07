from collections import defaultdict
from typing import Literal

from src.domain.entities.report import FileVulnerabilities, ReportStatus, SeverityInfo
from src.domain.exceptions.report import ReportNotFoundError
from src.domain.vaule_objects.pagination import Pagination
from src.domain.vaule_objects.vulnerability import Vulnerability
from src.ports.report_repo import IReportRepository, Report


class ReportService:
    def __init__(self, repository: IReportRepository) -> None:
        self._repo = repository

    async def get(self, id: str) -> Report:
        report = await self._repo.get(id=id)
        if not report:
            raise ReportNotFoundError()

        return report

    async def list(
        self,
        limit: int = 0,
        offset: int = 0,
        orderings: list[str] | None = None,
    ) -> list[Report]:
        return await self._repo.list(limit=limit, offset=offset, orderings=orderings)

    async def list_vulnerabilities(
        self,
        report_id: str,
        limit: int = 0,
        offset: int = 0,
        sort: Literal["severity", "file", "line"] | None = None,
        order: Literal["asc", "desc"] = "desc",
    ) -> Pagination[Vulnerability]:
        report = await self.get(id=report_id)
        if not report.vulnerabilities:
            return Pagination([], total=0)

        vulnerabilities = report.vulnerabilities[
            offset : offset + (limit or report.vulnerabilities_count)
        ]
        match sort:
            case "severity":
                vulnerabilities.sort(key=lambda v: v.severity, reverse=order == "desc")
            case "file":
                vulnerabilities.sort(key=lambda v: v.file, reverse=order == "desc")
            case "line":
                vulnerabilities.sort(key=lambda v: v.line, reverse=order == "desc")

        return Pagination(vulnerabilities, report.vulnerabilities_count)

    async def create(self) -> Report:
        report = Report()
        await self._repo.save(report)

        return report

    async def edit(
        self,
        report_id: str,
        status: ReportStatus | None = None,
        vulnerabilities: list[Vulnerability] | None = None,
    ) -> Report:
        report = await self.get(id=report_id)
        if status:
            report.status = status

        if vulnerabilities:
            report.vulnerabilities = vulnerabilities
            report.vulnerabilities_count = len(vulnerabilities)

            severity_counts = defaultdict(lambda: 0)
            files_count = defaultdict(lambda: 0)

            for vuln in vulnerabilities:
                severity_counts[vuln.severity] += 1
                files_count[vuln.file] += 1

            report.severity_distribution = SeverityInfo(**severity_counts)
            report.files_with_most_vulnerabilities = [
                FileVulnerabilities(file=item[0], count=item[1])
                for item in sorted(
                    files_count.items(), key=lambda i: i[1], reverse=True
                )
            ]

        await self._repo.save(report)

        return report
