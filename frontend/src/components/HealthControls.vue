<template>
  <section class="flex w-full flex-wrap items-center gap-3 rounded-xl border border-border bg-card px-4 py-3 shadow-soft">
    <StatusPill :latest-sample="latestSample" />
    <div class="flex items-baseline gap-2 rounded-md bg-muted px-3 py-1">
      <span class="text-xs uppercase tracking-[0.08em] text-muted-foreground">Polling</span>
      <span class="text-sm font-semibold text-foreground">{{ Math.round(pollIntervalMs / 1000) }}s</span>
    </div>
    <div class="flex items-center gap-2 rounded-md bg-muted px-3 py-1">
      <span class="text-xs text-muted-foreground">Auto-refresh</span>
      <Switch v-model="modelValue" />
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from "vue";
import Switch from "@/components/ui/Switch.vue";
import StatusPill from "./StatusPill.vue";
import type { HealthSample } from "@/lib/types";

const props = defineProps<{
  latestSample?: HealthSample;
  autoRefresh: boolean;
  pollIntervalMs: number;
}>();

const emit = defineEmits<{
  (e: "auto-refresh-change", value: boolean): void;
}>();

const modelValue = computed({
  get: () => props.autoRefresh,
  set: (value: boolean) => emit("auto-refresh-change", value),
});
</script>
