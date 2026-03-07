from litestar.dto import DataclassDTO, DTOConfig

from src.domain.entities.report import Report


class ReportStartOutDTO(DataclassDTO[Report]):
    config = DTOConfig(include={"id", "status"})


class ReportMetadataDTO(DataclassDTO[Report]):
    config = DTOConfig(exclude={"vulnerabilities"})


class ReportStatusDTO(DataclassDTO[Report]):
    config = DTOConfig(include={"status"})


class ReportStatsDTO(DataclassDTO[Report]):
    config = DTOConfig(
        include={"files_with_most_vulnerabilities", "severity_distribution"}
    )
