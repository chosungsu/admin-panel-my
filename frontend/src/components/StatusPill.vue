<template>
  <div :class="pillClass">
    <span class="text-sm font-semibold">{{ status.label }}</span>
    <span class="text-xs text-muted-foreground">latency {{ latency }}</span>
    <span class="text-xs text-muted-foreground">es {{ esStatus }}</span>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { HealthSample } from "@/lib/types";
import { cn } from "@/lib/utils";

const props = defineProps<{
  latestSample?: HealthSample;
}>();

const status = computed(() => {
  const sample = props.latestSample;
  if (!sample) return { label: "Collecting", tone: "neutral" };
  if (sample.ok) return { label: "Healthy", tone: "ok" };
  if (sample.statusText === "degraded") return { label: "Degraded", tone: "warn" };
  return { label: "Down", tone: "down" };
});

const pillClass = computed(() => {
  const tone = status.value.tone;
  const base = "inline-flex flex-wrap items-center gap-3 rounded-full border px-4 py-2";
  const toneClass =
    tone === "ok"
      ? "border-green-200 bg-green-50 text-green-700"
      : tone === "warn"
        ? "border-amber-200 bg-amber-50 text-amber-700"
        : tone === "down"
          ? "border-red-200 bg-red-50 text-red-700"
          : "border-border bg-muted text-foreground";
  return cn(base, toneClass);
});

const latency = computed(() => (props.latestSample ? `${props.latestSample.latencyMs}ms` : "--"));
const esStatus = computed(() => props.latestSample?.elasticsearch || "unknown");
</script>
