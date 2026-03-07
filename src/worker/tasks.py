from src.celery_app import app


# TODO: Реализовать
@app.task
def scan_archive(report_id: str, archive_path: str) -> None:
    raise NotImplementedError


@app.task
def scan_files(report_id: str, extracted_dir_path: str) -> None:
    raise NotImplementedError


@app.task
def call_ml(report_id: str, raw_findings: list[dict]) -> None:
    raise NotImplementedError


@app.task
def save_report(report_id: str, enriched_findings: list[dict]) -> None:
    raise NotImplementedError
