from litestar import Controller, get, post, status_codes

from src.application.dto.recommendations import RecommendationsGetDTO
from src.application.dto.reports import (
    ReportMetadataDTO,
    ReportStartOutDTO,
    ReportStatsDTO,
    ReportStatusDTO,
)
from src.application.dto.vulnerability import VulnerabilityGetDTO
from src.domain.aggregates.report import Report
from src.domain.vaule_objects.vulnerability import Vulnerability
from src.domain.vaule_objects.pagination import Pagination
from src.domain.vaule_objects.recommendations import Recommendations


class ReportController(Controller):
    path = "/reports"
    tags = ["Reports"]

    @post("/", return_dto=ReportStartOutDTO, status_code=status_codes.HTTP_202_ACCEPTED)
    async def start_report(self) -> Report:
        raise NotImplementedError

    @get("/{report_id:uuid}", return_dto=ReportMetadataDTO)
    async def get_report_metadata(self) -> Report:
        raise NotImplementedError

    @get("/{report_id:uuid}/status", return_dto=ReportStatusDTO)
    async def get_report_status(self) -> Report:
        raise NotImplementedError

    @get("/{report_id:uuid}/vulnerabilities", return_dto=VulnerabilityGetDTO)
    async def get_report_vulnerabilities(self) -> Pagination[Vulnerability]:
        raise NotImplementedError

    @get("/{report_id:uuid}/recommendations", return_dto=RecommendationsGetDTO)
    async def get_report_recommendations(self) -> Recommendations:
        raise NotImplementedError

    @get("/{report_id:uuid}/stats", return_dto=ReportStatsDTO)
    async def get_report_stats(self) -> Report:
        raise NotImplementedError
