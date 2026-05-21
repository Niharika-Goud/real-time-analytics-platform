from fastapi import APIRouter
from app.workers.report_tasks import generate_report

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.post("/generate")
async def generate():

    task = generate_report.delay()

    return {
        "task_id": task.id,
        "message": "Report generation started"
    }