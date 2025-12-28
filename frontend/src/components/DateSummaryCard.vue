<template>
  <section class="flex flex-1 flex-col gap-4 rounded-xl border border-border bg-card p-6 shadow-soft">
    <div class="flex items-start justify-between">
      <div>
        <h2 class="text-base font-semibold">Daily Summary</h2>
        <p class="desc text-sm text-muted-foreground">
          Failures and uptime for the selected day.
        </p>
      </div>
      <Button variant="outline" size="sm" @click="isDatePickerOpen = true" class="mt-0">
        <CalendarIcon class="h-4 w-4" />
      </Button>
    </div>
    <div class="space-y-3">
      <div
        ref="scrollContainerRef"
        class="metrics-scroll flex snap-x snap-mandatory gap-3 overflow-x-auto scroll-smooth scrollbar-hide"
        @scroll="handleScroll"
      >
        <div v-for="metric in METRICS" :key="metric.key" class="metric min-w-full snap-start rounded-lg border border-border bg-muted px-3 py-2">
          <div class="text-xs text-muted-foreground">{{ metric.label }}</div>
          <div class="text-sm font-semibold">
            {{ metric.key === 'failures' ? summary.failures : summary[metric.key] }}
          </div>
        </div>
      </div>
      <div class="metrics-dots flex justify-center gap-2">
        <button
          v-for="(_, index) in METRICS"
          :key="index"
          type="button"
          class="h-2 w-2 rounded-full"
          :class="index === currentMetricIndex ? 'bg-primary' : 'bg-border'"
          @click="handleDotClick(index)"
          :aria-label="`Show ${METRICS[index].label}`"
        />
      </div>
    </div>
    <Dialog v-model:open="isDatePickerOpen">
      <div class="space-y-4">
        <div>
          <h3 class="text-base font-semibold">Select Date</h3>
          <p class="text-sm text-muted-foreground">Choose a date to view the summary.</p>
        </div>
        <div class="space-y-2">
          <label class="text-sm font-medium">Date (YYYY-MM-DD)</label>
          <input
            ref="inputRef"
            type="date"
            :value="selectedDate"
            @change="onDateChange"
            class="w-full rounded-md border border-border bg-card px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-[var(--color-accent-weak)]"
          />
        </div>
        <div class="flex justify-end gap-2">
          <Button variant="outline" @click="isDatePickerOpen = false">Cancel</Button>
          <Button variant="gradient" @click="handleDateConfirm">Confirm</Button>
        </div>
      </div>
    </Dialog>
  </section>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import { Calendar as CalendarIcon } from "lucide-vue-next";
import Button from "@/components/ui/Button.vue";
import Dialog from "@/components/ui/Dialog.vue";
import type { HealthSample } from "@/lib/types";

const props = defineProps<{
  samples: HealthSample[];
}>();

const toDateKey = (value: string) => {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "";
  return new Intl.DateTimeFormat("en-CA", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(date);
};

const METRICS = [
  { key: "failures", label: "Failures" },
  { key: "failureRate", label: "Failure rate" },
  { key: "uptime", label: "Uptime" },
] as const;

const inputRef = ref<HTMLInputElement | null>(null);
const scrollContainerRef = ref<HTMLDivElement | null>(null);
const selectedDate = ref(toDateKey(new Date().toISOString()));
const currentMetricIndex = ref(0);
const isDatePickerOpen = ref(false);
const tempDate = ref(selectedDate.value);

const summary = computed(() => {
  const match = props.samples.find((sample) => toDateKey(sample.ts) === selectedDate.value);
  if (!match) {
    return { failures: "0/0", total: 0, failureRate: "--", uptime: "--" } as const;
  }
  const failures = match.failureCount ?? 0;
  const total = match.totalCount ?? 0;
  const failureRate = total ? `${Math.round((failures / total) * 100)}%` : "--";
  const uptime = total ? `${Math.round(((total - failures) / total) * 100)}%` : "--";
  return { failures: `${failures}/${total}`, total, failureRate, uptime } as const;
});

const onDateChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  tempDate.value = target.value;
};

const handleDateConfirm = () => {
  selectedDate.value = tempDate.value;
  isDatePickerOpen.value = false;
};

const handleScroll = (event: Event) => {
  const container = event.currentTarget as HTMLDivElement;
  const itemWidth = container.scrollWidth / METRICS.length;
  const newIndex = Math.round(container.scrollLeft / itemWidth);
  if (newIndex !== currentMetricIndex.value && newIndex >= 0 && newIndex < METRICS.length) {
    currentMetricIndex.value = newIndex;
  }
};

const handleDotClick = (index: number) => {
  currentMetricIndex.value = index;
  if (scrollContainerRef.value) {
    const metricElement = scrollContainerRef.value.children[index] as HTMLElement;
    metricElement.scrollIntoView({ behavior: "smooth", block: "nearest", inline: "center" });
  }
};
</script>

<style scoped>
.scrollbar-hide {
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
}

.scrollbar-hide::-webkit-scrollbar {
  display: none; /* Chrome, Safari and Opera */
}

@media (min-width: 700px) and (max-width: 1100px) {
  .desc {
    display: none;
  }
}

@media (min-width: 700px) and (max-width: 750px) {
  .metrics-scroll {
    flex-direction: column;
    overflow-x: visible;
    overflow-y: visible;
    scroll-snap-type: none;
  }

  .metric {
    min-width: 0;
    width: 100%;
  }

  .metrics-dots {
    display: none;
  }
}
</style>
