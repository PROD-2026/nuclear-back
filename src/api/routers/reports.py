from typing import Annotated, Literal
from uuid import UUID

from litestar import Controller, get, post, status_codes
from litestar.enums import RequestEncodingType
from litestar.params import Body
from punq import Container

from src.application.dto.recommendations import RecommendationsGetDTO
from src.application.dto.reports import (
    ReportMetadataDTO,
    ReportStartOutDTO,
    ReportStatsDTO,
    ReportStatusDTO,
)
from src.application.services.uploads import UploadsService
from src.domain.entities.report import Report, Vulnerability
from src.domain.vaule_objects.pagination import Pagination
from src.domain.vaule_objects.recommendations import Recommendations
from src.domain.vaule_objects.report import ReportIn
from src.infrastructure.container import ReportService


class ReportController(Controller):
    path = "/reports"
    tags = ["Reports"]

    @post(
        "/",
        return_dto=ReportStartOutDTO,
        status_code=status_codes.HTTP_202_ACCEPTED,
    )
    async def start_report(
        self,
        data: Annotated[ReportIn, Body(media_type=RequestEncodingType.MULTI_PART)],
        container: Container,
    ) -> Report:
        uploads_service: UploadsService = container.resolve(UploadsService)
        report_service: ReportService = container.resolve(ReportService)

        report = await report_service.create()

        await uploads_service.upload_project(
            report_id=report.id, data=await data.file.read()
        )

        # TODO: send actual job to Celery

        return report

    @get("/{report_id:uuid}", return_dto=ReportMetadataDTO)
    async def get_report_metadata(
        self, report_id: UUID, container: Container
    ) -> Report:
        report_service: ReportService = container.resolve(ReportService)

        return await report_service.get(id=str(report_id))

    @get("/{report_id:uuid}/status", return_dto=ReportStatusDTO)
    async def get_report_status(self, report_id: UUID, container: Container) -> Report:
        report_service: ReportService = container.resolve(ReportService)

        return await report_service.get(id=str(report_id))

    @get("/{report_id:uuid}/vulnerabilities")
    async def get_report_vulnerabilities(
        self,
        container: Container,
        report_id: UUID,
        sort: Literal["severity", "file", "line"] = "severity",
        order: Literal["asc", "desc"] = "desc",
        limit: int = 50,
        offset: int = 0,
    ) -> Pagination[Vulnerability]:
        report_service: ReportService = container.resolve(ReportService)
        return await report_service.list_vulnerabilities(
            report_id=str(report_id), limit=limit, offset=offset, sort=sort, order=order
        )

    @get("/{report_id:uuid}/recommendations", return_dto=RecommendationsGetDTO)
    async def get_report_recommendations(
        self, report_id: UUID, container: Container, use_llm: bool = False
    ) -> Recommendations:
        report_service: ReportService = container.resolve(ReportService)
        return Recommendations(text="TODO!")

    @get("/{report_id:uuid}/stats", return_dto=ReportStatsDTO)
    async def get_report_stats(self, report_id: UUID, container: Container) -> Report:
        report_service: ReportService = container.resolve(ReportService)

        return await report_service.get(id=str(report_id))
