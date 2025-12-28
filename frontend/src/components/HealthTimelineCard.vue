<template>
  <section class="flex flex-col gap-6 rounded-xl border border-border bg-card p-6 shadow-soft">
    <div>
      <h2 class="text-lg font-semibold">Health Timeline</h2>
      <p class="text-sm text-muted-foreground">
        Last {{ maxPoints }} days - every {{ Math.round(pollIntervalMs / 1000) }}s check
      </p>
    </div>

    <div v-if="isLoading && samples.length === 0" class="grid gap-3">
      <div class="text-sm text-muted-foreground">Collecting health samples...</div>
      <div class="h-3 rounded-full bg-gradient-to-r from-muted via-border to-muted animate-pulse" />
    </div>

    <div
      v-else
      class="grid gap-2"
      :style="{
        gridTemplateColumns: `repeat(${gridConfig.columns}, minmax(4px, 1fr))`,
        gridTemplateRows: `repeat(${gridConfig.rows}, 1fr)`
      }"
    >
      <div
        v-for="(sample, index) in paddedSamples"
        :key="sample?.ts || `empty-${index}`"
        :class="pointClass(sample)"
      >
        <Tooltip v-if="sample">
          <template #trigger>
            <div class="h-full w-full" />
          </template>
          <div class="space-y-1">
            <div class="font-semibold">{{ formatTimestamp(sample.ts) }}</div>
            <div>weekday: {{ formatWeekday(sample.ts) }}</div>
            <div>status: {{ sample.statusText }}</div>
            <div>failures: {{ sample.failureCount ?? 0 }}/{{ sample.totalCount ?? 0 }}</div>
            <div>es: {{ sample.elasticsearch }}</div>
            <div>latency: {{ sample.latencyMs }}ms</div>
          </div>
        </Tooltip>
      </div>
    </div>

    <div class="grid gap-3 border-t border-border pt-4 md:grid-cols-3">
      <div>
        <div class="text-xs uppercase tracking-[0.08em] text-muted-foreground">Latest</div>
        <div class="text-sm font-semibold">{{ latestSample ? formatTimestamp(latestSample.ts) : "--" }}</div>
      </div>
      <div>
        <div class="text-xs uppercase tracking-[0.08em] text-muted-foreground">Latency</div>
        <div class="text-sm font-semibold">{{ latestSample ? `${latestSample.latencyMs}ms` : "--" }}</div>
      </div>
      <div>
        <div class="text-xs uppercase tracking-[0.08em] text-muted-foreground">Elasticsearch</div>
        <div class="text-sm font-semibold">{{ latestSample?.elasticsearch || "--" }}</div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, watch } from "vue";
import Tooltip from "@/components/ui/Tooltip.vue";
import type { HealthSample } from "@/lib/types";
import { useToast } from "@/composables/useToast";
import { cn } from "@/lib/utils";

const props = defineProps<{
  samples: HealthSample[];
  maxPoints: number;
  pollIntervalMs: number;
  isLoading: boolean;
  lastError: string | null;
  lastErrorAt: Date | null;
}>();

const { showToast } = useToast();

const userTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;

const formatTimestamp = (value: string) => {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "Unknown";
  return new Intl.DateTimeFormat(undefined, {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    timeZone: userTimeZone,
  }).format(date);
};

const formatWeekday = (value: string) => {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "Unknown";
  return new Intl.DateTimeFormat(undefined, {
    weekday: "short",
    timeZone: userTimeZone,
  }).format(date);
};

const getTone = (sample?: HealthSample | null) => {
  if (!sample) return "empty";
  if (sample.ok) return "ok";
  if (sample.statusText === "degraded") return "warn";
  return "down";
};

const latestSample = computed(() => props.samples[props.samples.length - 1]);

const paddedSamples = computed(() => {
  const missing = Math.max(0, props.maxPoints - props.samples.length);
  const padding = Array.from({ length: missing }, () => null);
  return [...padding, ...props.samples.slice(-props.maxPoints)];
});

const gridConfig = computed(() => {
  if (props.maxPoints === 30) {
    return { columns: 10, rows: 3 };
  }
  if (props.maxPoints === 60) {
    return { columns: 12, rows: 5 };
  }
  if (props.maxPoints === 90) {
    return { columns: 18, rows: 5 };
  }
  const columns = Math.ceil(Math.sqrt(props.maxPoints * 1.5));
  const rows = Math.ceil(props.maxPoints / columns);
  return { columns, rows };
});

const pointClass = (sample?: HealthSample | null) => {
  const tone = getTone(sample);
  const base = "h-2 w-full rounded-full";
  const toneClass =
    tone === "ok"
      ? "bg-green-500"
      : tone === "warn"
        ? "bg-amber-400"
        : tone === "down"
          ? "bg-red-500"
          : "bg-slate-300";
  return cn(base, toneClass);
};

const formatDateTime = (value: Date | null) => {
  if (!value) return "--";
  return new Intl.DateTimeFormat(undefined, {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    timeZone: userTimeZone,
  }).format(value);
};

watch(
  () => [props.lastError, props.lastErrorAt],
  ([error, errorAt]) => {
    if (error && errorAt) {
      showToast(`${error} Last attempt ${formatDateTime(errorAt)}`, "error");
    }
  }
);
</script>
