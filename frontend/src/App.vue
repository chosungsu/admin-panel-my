<template>
  <div class="h-screen bg-background text-foreground overflow-hidden">
    <Topbar
      title="Console"
      subtitle=""
      :projects="projects"
      :selected-project-id="selectedProjectId"
      @project-change="setSelectedProject"
    />
    <main class="flex min-h-0 flex-col gap-5 overflow-y-auto overflow-x-hidden px-8 py-4 scrollbar-hide" style="height: calc(100vh - 64px); margin-top: 64px; z-index: 40;">
      <HealthControls
        :latest-sample="latestSample"
        :auto-refresh="autoRefresh"
        :poll-interval-ms="pollIntervalMs"
        @auto-refresh-change="handleAutoRefreshChange"
      />
      <div class="grid grid-cols-[minmax(0,2fr)_minmax(0,1fr)] gap-5">
        <div class="flex min-h-0 flex-col gap-5">
          <HealthTimelineCard
            :samples="samples"
            :max-points="displayPoints"
            :poll-interval-ms="pollIntervalMs"
            :is-loading="isLoading"
            :last-error="lastError"
            :last-error-at="lastErrorAt"
          />
          <HealthResultsTable :rows="resultRows" />
        </div>
        <div class="flex min-h-0 flex-col gap-5">
          <DateSummaryCard :samples="samples" />
          <PollingIntervalCard
            :current-interval-ms="pollIntervalMs"
            :on-update="handlePollingIntervalUpdate"
          />
          <DeleteResultsCard
            :project-name="selectedProjectId"
            :on-delete="handleDeleteResults"
          />
        </div>
      </div>
    </main>
    <ToastContainer />
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
import Topbar from "@/components/Topbar.vue";
import HealthControls from "@/components/HealthControls.vue";
import HealthTimelineCard from "@/components/HealthTimelineCard.vue";
import PollingIntervalCard from "@/components/PollingIntervalCard.vue";
import DeleteResultsCard from "@/components/DeleteResultsCard.vue";
import DateSummaryCard from "@/components/DateSummaryCard.vue";
import HealthResultsTable from "@/components/HealthResultsTable.vue";
import ToastContainer from "@/components/ToastContainer.vue";
import {
  fetchHealthPeriod,
  fetchHealthSettings,
  fetchHealthResultsRows,
  truncateHealthResults,
  updateHealthSettings,
} from "@/lib/api";
import type { HealthSample, Project } from "@/lib/types";

const DEFAULT_PROJECT: Project = {
  id: "paper-service",
  name: "Paper Service",
  baseUrl: "http://localhost:8000",
};

const env = import.meta.env as unknown as Record<string, string>;
const POLL_INTERVAL_MS = Number(env.VITE_POLL_INTERVAL_MS || 60000);
const HEALTH_TIMEOUT_MS = Number(env.VITE_HEALTH_TIMEOUT_MS || 2500);
const MAX_POINTS = 90;
const PROJECTS_JSON = env.VITE_PROJECTS_JSON || env.NEXT_PUBLIC_PROJECTS_JSON || "";

function parseProjects(jsonValue: string): Project[] {
  if (!jsonValue) return [DEFAULT_PROJECT];
  try {
    const parsed = JSON.parse(jsonValue);
    if (!Array.isArray(parsed)) return [DEFAULT_PROJECT];
    return parsed
      .map((item) => ({
        id: item.id || item.project_id || DEFAULT_PROJECT.id,
        name: item.name || item.project_name || DEFAULT_PROJECT.name,
        baseUrl: item.baseUrl || item.base_url || DEFAULT_PROJECT.baseUrl,
      }))
      .filter((project) => project.id && project.baseUrl);
  } catch (error) {
    return [DEFAULT_PROJECT];
  }
}

function parseTimestamp(value: string): Date | null {
  if (!value) return null;
  const trimmed = value.trim();
  const hasZone = /[zZ]|[+-]\d{2}:\d{2}$/.test(trimmed);
  if (hasZone) {
    const direct = new Date(trimmed);
    return Number.isNaN(direct.getTime()) ? null : direct;
  }
  const normalized = trimmed.includes("T") ? trimmed : trimmed.replace(" ", "T");
  const assumedUtc = `${normalized}Z`;
  const parsed = new Date(assumedUtc);
  return Number.isNaN(parsed.getTime()) ? null : parsed;
}

function normalizeHealthResults(items: Array<Record<string, unknown>>): HealthSample[] {
  return items
    .map((item) => {
      const statusText = String(item.status_text || item.status || "unknown");
      const elasticsearch = String(item.elasticsearch || "unknown");
      const ok = Boolean(item.ok ?? (statusText === "ok" && elasticsearch === "connected"));
      const ts = (item.created_at as string) || (item.createdAt as string) || "";
      const date = parseTimestamp(ts);
      if (!date) return null;
      return {
        ts: date.toISOString(),
        ok,
        statusText,
        elasticsearch,
        latencyMs: Number(item.latency_ms || 0),
        failureCount: Number(item.failure_count ?? 0),
        totalCount: Number(item.total_count ?? 0),
      };
    })
    .filter((item): item is NonNullable<typeof item> => item !== null)
    .sort((a, b) => a.ts.localeCompare(b.ts));
}

const projects = ref(parseProjects(PROJECTS_JSON));
const defaultProjectId =
  projects.value.find((project) => project.id === "paper-service")?.id ||
  projects.value[0]?.id ||
  "";
const selectedProjectId = ref(defaultProjectId);
const samples = ref<HealthSample[]>([]);
const resultRows = ref<Array<Record<string, unknown>>>([]);
const autoRefresh = ref(true);
const pollIntervalMs = ref(POLL_INTERVAL_MS);
const maxPoints = ref(MAX_POINTS);
const displayPoints = ref(MAX_POINTS);
const isLoading = ref(true);
const lastError = ref<string | null>(null);
const lastErrorAt = ref<Date | null>(null);
const inFlight = ref(false);
const settingsInFlight = ref(false);

const selectedProject = computed(
  () => projects.value.find((project) => project.id === selectedProjectId.value) || projects.value[0]
);

const latestSample = computed(() => samples.value[samples.value.length - 1]);

const loadHealthResults = async () => {
  if (!selectedProject.value || inFlight.value) return;
  inFlight.value = true;
  try {
    const [periodData, rowsData] = await Promise.all([
      fetchHealthPeriod(selectedProject.value.id, maxPoints.value, HEALTH_TIMEOUT_MS),
      fetchHealthResultsRows(selectedProject.value.id, 5, HEALTH_TIMEOUT_MS),
    ]);
    const normalized = normalizeHealthResults(periodData.results as Array<Record<string, unknown>>);
    samples.value = normalized.slice(-maxPoints.value);
    resultRows.value = rowsData.results as Array<Record<string, unknown>>;
    lastError.value = null;
    isLoading.value = false;
  } catch (error) {
    lastError.value = "Failed to fetch";
    lastErrorAt.value = new Date();
    isLoading.value = false;
  } finally {
    inFlight.value = false;
  }
};

const loadSettings = async () => {
  if (!selectedProject.value || settingsInFlight.value) return;
  settingsInFlight.value = true;
  try {
    const settings = await fetchHealthSettings(selectedProject.value.id, HEALTH_TIMEOUT_MS);
    pollIntervalMs.value = settings.polling_interval_ms || POLL_INTERVAL_MS;
    autoRefresh.value = settings.auto_refresh;
    maxPoints.value = MAX_POINTS;
  } catch (error) {
    pollIntervalMs.value = POLL_INTERVAL_MS;
    autoRefresh.value = true;
    maxPoints.value = MAX_POINTS;
  } finally {
    settingsInFlight.value = false;
  }
};

const setSelectedProject = (value: string) => {
  selectedProjectId.value = value;
};

watch(
  () => selectedProjectId.value,
  async () => {
    samples.value = [];
    isLoading.value = true;
    lastError.value = null;
    lastErrorAt.value = null;
    await loadSettings();
    await loadHealthResults();
  },
  { immediate: true }
);

let intervalId: number | null = null;
watch([autoRefresh, pollIntervalMs, selectedProjectId], () => {
  if (intervalId) {
    window.clearInterval(intervalId);
    intervalId = null;
  }
  if (autoRefresh.value) {
    intervalId = window.setInterval(loadHealthResults, pollIntervalMs.value);
  }
});

const updateDisplayPoints = () => {
  if (typeof window === "undefined") return;
  const width = window.innerWidth;
  if (width <= 800) {
    displayPoints.value = 30;
  } else if (width <= 1200) {
    displayPoints.value = 60;
  } else {
    displayPoints.value = 90;
  }
};

onMounted(() => {
  updateDisplayPoints();
  window.addEventListener("resize", updateDisplayPoints);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", updateDisplayPoints);
  if (intervalId) {
    window.clearInterval(intervalId);
  }
});

const handleAutoRefreshChange = async (nextValue: boolean) => {
  if (!selectedProject.value) return;
  autoRefresh.value = nextValue;
  try {
    const updated = await updateHealthSettings(
      { project_name: selectedProject.value.id, auto_refresh: nextValue },
      HEALTH_TIMEOUT_MS
    );
    autoRefresh.value = updated.auto_refresh;
  } catch (error) {
    autoRefresh.value = nextValue;
  }
};

const handlePollingIntervalUpdate = async (intervalMs: number) => {
  if (!selectedProject.value) return;
  pollIntervalMs.value = intervalMs;
  try {
    await updateHealthSettings(
      { project_name: selectedProject.value.id, polling_interval_ms: intervalMs },
      HEALTH_TIMEOUT_MS
    );
  } catch (error) {
    // Caller handles messaging.
  }
};

const handleDeleteResults = async () => {
  if (!selectedProject.value) return;
  await truncateHealthResults(selectedProject.value.id, HEALTH_TIMEOUT_MS);
  samples.value = [];
  isLoading.value = true;
  await loadHealthResults();
};
</script>

<style scoped>
main.scrollbar-hide {
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
}

main.scrollbar-hide::-webkit-scrollbar {
  display: none; /* Chrome, Safari and Opera */
}

@media (max-width: 720px) {
  main {
    height: calc(100vh - 64px) !important;
    min-height: calc(100vh - 64px);
    padding-left: 20px;
    padding-right: 20px;
    padding-bottom: 32px;
    overflow-y: auto;
    overflow-x: hidden;
    -ms-overflow-style: none !important;
    scrollbar-width: none !important;
  }

  main.scrollbar-hide {
    -ms-overflow-style: none !important;
    scrollbar-width: none !important;
  }

  main.scrollbar-hide::-webkit-scrollbar {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
  }

  main > div {
    grid-template-columns: minmax(0, 1fr) !important;
    min-height: auto;
    height: auto;
  }

  main > div > div {
    min-height: auto;
    height: auto;
  }
}
</style>
