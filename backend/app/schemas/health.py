from typing import List, Optional

from pydantic import BaseModel


class HealthPeriodItem(BaseModel):
    id: int
    created_at: str
    ok: bool
    status_text: str
    elasticsearch: str
    latency_ms: int
    failure_count: int
    total_count: int


class HealthPeriodResponse(BaseModel):
    project_name: str
    limit: int
    results: List[HealthPeriodItem]


class HealthSettingsResponse(BaseModel):
    project_name: str
    polling_interval_ms: int
    auto_refresh: bool
    max_points: int


class HealthSettingsUpdate(BaseModel):
    project_name: str
    polling_interval_ms: Optional[int] = None
    auto_refresh: Optional[bool] = None
    max_points: Optional[int] = None


class HealthTruncateRequest(BaseModel):
    project_name: str


class HealthResultRow(BaseModel):
    id: int
    project_name: str
    created_at: str
    ok: bool
    status_text: str
    elasticsearch: str
    latency_ms: int


class HealthResultsResponse(BaseModel):
    project_name: str
    limit: int
    results: List[HealthResultRow]
