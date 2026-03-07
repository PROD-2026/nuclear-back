import asyncio

from src.application.services.report import ReportService
from src.application.services.scanner import ScannerService
from src.application.use_cases.scan import perform_scan
from src.celery_app import app
from src.infrastructure.container import build_container


@app.task
def make_report(report_id: str, whitelist: list[str], blacklist: list[str]) -> None:
    container = build_container()
    scanner: ScannerService = container.resolve(ScannerService)
    report_service: ReportService = container.resolve(ReportService)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        perform_scan(scanner, report_service, report_id, whitelist, blacklist)
    )
