export type Project = {
  id: string;
  name: string;
  baseUrl: string;
};

export type HealthSample = {
  ts: string;
  ok: boolean;
  statusText: string;
  elasticsearch: string;
  latencyMs: number;
  failureCount?: number;
  totalCount?: number;
};
