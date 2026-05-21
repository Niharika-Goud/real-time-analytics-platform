from pathlib import Path

from app.workers.celery_worker import celery


@celery.task
def generate_report():

    reports_dir = Path("reports")

    reports_dir.mkdir(exist_ok=True)

    report_path = reports_dir / "report.txt"

    with open(report_path, "w") as file:
        file.write("Analytics Report Generated Successfully")

    return {
        "status": "success",
        "path": str(report_path)
    }