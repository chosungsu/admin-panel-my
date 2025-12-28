import os


def get_settings() -> dict:
  return {
    "database_url": os.getenv(
      "DATABASE_URL", "postgresql+psycopg2://console:console2026@postgres:5432/appdb"
    ),
    "app_env": os.getenv("APP_ENV", "local"),
    "log_level": os.getenv("LOG_LEVEL", "info"),
    "service_name": os.getenv("SERVICE_NAME", "paper-service"),
    "elasticsearch_status": os.getenv("ELASTICSEARCH_STATUS", "connected"),
  }
