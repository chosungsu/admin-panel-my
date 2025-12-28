export type HealthPeriodItem = {
  id: number;
  created_at: string;
  ok: boolean;
  status_text: string;
  elasticsearch: string;
  latency_ms: number;
  failure_count: number;
  total_count: number;
};

export type HealthPeriodResponse = {
  project_name: string;
  limit: number;
  results: HealthPeriodItem[];
};

export type HealthSettingsResponse = {
  project_name: string;
  polling_interval_ms: number;
  auto_refresh: boolean;
  max_points: number;
};

export type HealthSettingsUpdate = Partial<HealthSettingsResponse> & { project_name: string };

export async function fetchHealthPeriod(
  projectName: string,
  limit: number,
  timeoutMs: number,
  since?: string
): Promise<HealthPeriodResponse> {
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), timeoutMs);
  try {
    const params = new URLSearchParams({ project_name: projectName, limit: String(limit) });
    if (since) params.set("since", since);
    const response = await fetch(`/api/health/period?${params.toString()}`, {
      signal: controller.signal,
    });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return await response.json();
  } finally {
    window.clearTimeout(timeoutId);
  }
}

export async function fetchHealthSettings(
  projectName: string,
  timeoutMs: number
): Promise<HealthSettingsResponse> {
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), timeoutMs);
  try {
    const params = new URLSearchParams({ project_name: projectName });
    const response = await fetch(`/api/settings/health-polling?${params.toString()}`, {
      signal: controller.signal,
    });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return await response.json();
  } finally {
    window.clearTimeout(timeoutId);
  }
}

export async function updateHealthSettings(
  payload: HealthSettingsUpdate,
  timeoutMs: number
): Promise<HealthSettingsResponse> {
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(`/api/settings/health-polling`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      signal: controller.signal,
    });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return await response.json();
  } finally {
    window.clearTimeout(timeoutId);
  }
}

export async function truncateHealthResults(
  projectName: string,
  timeoutMs: number
): Promise<void> {
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(`/api/health/results/truncate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ project_name: projectName }),
      signal: controller.signal,
    });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
  } finally {
    window.clearTimeout(timeoutId);
  }
}

export type HealthResultRow = {
  id: number;
  project_name: string;
  created_at: string;
  ok: boolean;
  status_text: string;
  elasticsearch: string;
  latency_ms: number;
};

export type HealthResultsResponse = {
  project_name: string;
  limit: number;
  results: HealthResultRow[];
};

export async function fetchHealthResultsRows(
  projectName: string,
  limit: number,
  timeoutMs: number
): Promise<HealthResultsResponse> {
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), timeoutMs);
  try {
    const params = new URLSearchParams({ project_name: projectName, limit: String(limit) });
    const response = await fetch(`/api/health/results?${params.toString()}`, {
      signal: controller.signal,
    });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return await response.json();
  } finally {
    window.clearTimeout(timeoutId);
  }
}
