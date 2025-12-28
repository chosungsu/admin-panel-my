import os
import logging
from pathlib import Path

# .env 파일 로드 (로컬 개발 환경용)
try:
    from dotenv import load_dotenv
    # 프로젝트 루트 디렉토리 찾기 (backend/app/core/config.py에서 3단계 위)
    env_path = Path(__file__).parent.parent.parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    # python-dotenv가 없어도 동작하도록
    pass

logger = logging.getLogger(__name__)


def get_database_url() -> str:
    """
    환경에 따라 적절한 데이터베이스 URL을 반환합니다.
    - DATABASE_URL이 직접 설정되어 있으면 그것을 사용
    - APP_ENV가 "production"이면 DATABASE_URL_INTERNAL 사용 (내부 네트워크)
    - 그 외에는 DATABASE_URL_EXTERNAL 사용 (외부 접근)
    """
    # 직접 설정된 DATABASE_URL이 있으면 우선 사용
    direct_url = os.getenv("DATABASE_URL")
    if direct_url:
        return direct_url
    
    app_env = os.getenv("APP_ENV", "local")
    
    # 배포 환경(production)에서는 Internal URL 사용
    internal_url = None
    if app_env == "production":
        internal_url = os.getenv("DATABASE_URL_INTERNAL")
        if internal_url:
            # Internal URL에 psycopg2 드라이버 추가 (없는 경우)
            if not internal_url.startswith("postgresql+psycopg2://"):
                internal_url = internal_url.replace("postgresql://", "postgresql+psycopg2://")
            logger.info(f"Using DATABASE_URL_INTERNAL (APP_ENV={app_env})")
            return internal_url
    
    # 로컬 환경에서는 External URL 사용
    external_url = os.getenv("DATABASE_URL_EXTERNAL")
    if external_url:
        # External URL에 psycopg2 드라이버 추가 (없는 경우)
        if not external_url.startswith("postgresql+psycopg2://"):
            external_url = external_url.replace("postgresql://", "postgresql+psycopg2://")
        logger.info(f"Using DATABASE_URL_EXTERNAL (APP_ENV={app_env})")
        return external_url
    
    # 디버깅: 어떤 환경 변수가 설정되어 있는지 확인
    logger.warning(
        f"Database URL not found. "
        f"DATABASE_URL={bool(direct_url)}, "
        f"DATABASE_URL_INTERNAL={bool(internal_url)}, "
        f"DATABASE_URL_EXTERNAL={bool(external_url)}, "
        f"APP_ENV={app_env}"
    )
    
    # 둘 다 없으면 빈 문자열 반환
    return ""


def get_settings() -> dict:
  return {
    "database_url": get_database_url(),
    "app_env": os.getenv("APP_ENV", "local"),
    "log_level": os.getenv("LOG_LEVEL", "info"),
    "service_name": os.getenv("SERVICE_NAME", "paper-service"),
    "elasticsearch_status": os.getenv("ELASTICSEARCH_STATUS", "connected"),
  }
