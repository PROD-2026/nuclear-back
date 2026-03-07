import logging

from src.application.services.report import ReportService
from src.application.services.scanner import ScannerService
from src.domain.aggregates.report import ReportStatus


async def perform_scan(
    scanner_service: ScannerService,
    report_service: ReportService,
    report_id: str,
    whitelist: list[str],
    blacklist: list[str],
) -> None:
    await report_service.edit(report_id=report_id, status=ReportStatus.SCANNING)

    vulnerabilities = await scanner_service.found_vulnerabilities(
        report_id=report_id, whitelist=whitelist, blacklist=blacklist
    )
    try:
        vulnerabilities = await scanner_service.check_by_ml(
            vulnerabilities=vulnerabilities
        )
    except Exception as e:
        logging.error(f"Unable to recheck scan with ML: {e}")

    vulnerabilities = scanner_service.mask_values(vulnerabilities)

    await report_service.edit(
        report_id=report_id,
        status=ReportStatus.DONE,
        vulnerabilities=vulnerabilities,
    )
