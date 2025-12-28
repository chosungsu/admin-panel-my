from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.health_result import HealthResult
from app.models.health_setting import HealthSetting

from app.schemas.health import (
    HealthPeriodItem,
    HealthPeriodResponse,
    HealthResultRow,
    HealthResultsResponse,
    HealthSettingsResponse,
    HealthSettingsUpdate,
    HealthTruncateRequest,
)

router = APIRouter()
MAX_HEALTH_DAYS = 90


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def parse_since(value: str | None) -> datetime | None:
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


@router.get("/health/period", response_model=HealthPeriodResponse)
def get_health_period(
    project_name: str = Query(...),
    limit: int = Query(MAX_HEALTH_DAYS, ge=1, le=500),
    since: str | None = Query(None),
    order: str = Query("desc"),
    db: Session = Depends(get_db),
):
    since_dt = parse_since(since)
    effective_limit = min(limit, MAX_HEALTH_DAYS)

    cutoff_date = (datetime.now(timezone.utc) - timedelta(days=MAX_HEALTH_DAYS)).date()
    db.query(HealthResult).filter(
        HealthResult.project_name == project_name,
        func.date(HealthResult.created_at) < cutoff_date,
    ).delete(synchronize_session=False)
    db.commit()

    day_col = func.date(HealthResult.created_at).label("day")
    failure_count_col = func.sum(
        case((HealthResult.ok.is_(False), 1), else_=0)
    ).label("failure_count")
    total_count_col = func.count(HealthResult.id).label("total_count")
    es_ok_col = func.bool_and(HealthResult.elasticsearch == "connected").label("es_ok")
    latency_col = func.max(HealthResult.latency_ms).label("latency_ms")
    id_col = func.min(HealthResult.id).label("id")

    query = db.query(
        day_col,
        id_col,
        failure_count_col,
        total_count_col,
        es_ok_col,
        latency_col,
    ).filter(
        HealthResult.project_name == project_name
    )
    if since_dt:
        query = query.filter(HealthResult.created_at >= since_dt)
    query = query.group_by(day_col)
    if order.lower() == "asc":
        query = query.order_by(day_col.asc())
    else:
        query = query.order_by(day_col.desc())
    rows = query.limit(effective_limit).all()
    return {
        "project_name": project_name,
        "limit": effective_limit,
        "results": [
            HealthPeriodItem(
                id=row.id,
                created_at=datetime.combine(row.day, datetime.min.time(), tzinfo=timezone.utc)
                .isoformat()
                .replace("+00:00", "Z"),
                ok=bool(row.failure_count == 0),
                status_text="ok" if row.failure_count == 0 else "error",
                elasticsearch="connected" if row.es_ok else "disconnected",
                latency_ms=int(row.latency_ms or 0),
                failure_count=int(row.failure_count or 0),
                total_count=int(row.total_count or 0),
            )
            for row in rows
        ],
    }


@router.get("/settings/health-polling", response_model=HealthSettingsResponse)
def get_health_settings(project_name: str = Query(...), db: Session = Depends(get_db)):
    settings = (
        db.query(HealthSetting).filter(HealthSetting.project_name == project_name).first()
    )
    if not settings:
        settings = HealthSetting(project_name=project_name)
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return {
        "project_name": settings.project_name,
        "polling_interval_ms": settings.polling_interval_ms,
        "auto_refresh": settings.auto_refresh,
        "max_points": settings.max_points,
    }


@router.put("/settings/health-polling", response_model=HealthSettingsResponse)
def update_health_settings(payload: HealthSettingsUpdate, db: Session = Depends(get_db)):
    settings = (
        db.query(HealthSetting).filter(HealthSetting.project_name == payload.project_name).first()
    )
    if not settings:
        settings = HealthSetting(project_name=payload.project_name)
        db.add(settings)
    if payload.polling_interval_ms is not None:
        settings.polling_interval_ms = payload.polling_interval_ms
    if payload.auto_refresh is not None:
        settings.auto_refresh = payload.auto_refresh
    if payload.max_points is not None:
        settings.max_points = payload.max_points
    settings.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(settings)
    return {
        "project_name": settings.project_name,
        "polling_interval_ms": settings.polling_interval_ms,
        "auto_refresh": settings.auto_refresh,
        "max_points": settings.max_points,
    }


@router.post("/health/results/truncate")
def truncate_health_results(payload: HealthTruncateRequest, db: Session = Depends(get_db)):
    if not payload.project_name:
        raise HTTPException(status_code=400, detail="project_name is required")
    db.query(HealthResult).filter(HealthResult.project_name == payload.project_name).delete()
    db.commit()
    return {"status": "ok"}


@router.get("/health/results", response_model=HealthResultsResponse)
def get_health_results(
    project_name: str = Query(...),
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db),
):
    rows = (
        db.query(HealthResult)
        .filter(HealthResult.project_name == project_name)
        .order_by(HealthResult.created_at.desc())
        .limit(limit)
        .all()
    )
    return {
        "project_name": project_name,
        "limit": limit,
        "results": [
            HealthResultRow(
                id=row.id,
                project_name=row.project_name,
                created_at=(
                    row.created_at.replace(tzinfo=timezone.utc)
                    if row.created_at.tzinfo is None
                    else row.created_at.astimezone(timezone.utc)
                )
                .isoformat()
                .replace("+00:00", "Z"),
                ok=row.ok,
                status_text=row.status_text,
                elasticsearch=row.elasticsearch,
                latency_ms=row.latency_ms,
            )
            for row in rows
        ],
    }
