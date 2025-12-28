<template>
  <header class="fixed top-0 left-0 right-0 z-50 flex h-16 items-center justify-between gap-6 border-b border-border bg-card px-8 shadow-soft header-responsive">
    <div class="min-w-0">
      <div class="truncate text-lg font-bold tracking-tight text-foreground">{{ title }}</div>
      <div v-if="subtitle" class="text-xs uppercase tracking-[0.08em] text-muted-foreground">{{ subtitle }}</div>
    </div>
    <div class="flex items-center gap-3">
      <button
        type="button"
        class="inline-flex h-9 w-9 items-center justify-center rounded-md border border-border bg-card text-muted-foreground transition hover:bg-muted"
        @click="toggleTheme"
        :aria-label="themeLabel"
        :title="themeLabel"
      >
        <component :is="themeIcon" class="h-4 w-4" />
      </button>
      <ProjectSwitcher
        :projects="projects"
        :selected-project-id="selectedProjectId"
        @project-change="emit('project-change', $event)"
      />
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { Moon, Sun } from "lucide-vue-next";
import ProjectSwitcher from "./ProjectSwitcher.vue";
import type { Project } from "@/lib/types";

const props = defineProps<{
  title: string;
  subtitle: string;
  projects: Project[];
  selectedProjectId: string;
}>();

const emit = defineEmits<{
  (e: "project-change", value: string): void;
}>();

const theme = ref<"light" | "dark">("light");

onMounted(() => {
  if (typeof window === "undefined") return;
  const stored = localStorage.getItem("theme") as "light" | "dark" | null;
  if (stored) {
    theme.value = stored;
  } else {
    theme.value = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
});

watch(
  theme,
  (value) => {
    if (typeof document !== "undefined") {
      document.documentElement.setAttribute("data-theme", value);
      localStorage.setItem("theme", value);
    }
  },
  { immediate: true }
);

const toggleTheme = () => {
  theme.value = theme.value === "light" ? "dark" : "light";
};

const themeLabel = computed(() =>
  theme.value === "light" ? "Switch to dark mode" : "Switch to light mode"
);

const themeIcon = computed(() => (theme.value === "light" ? Moon : Sun));
</script>

<style scoped>
@media (max-width: 720px) {
  .header-responsive {
    padding-left: 20px;
    padding-right: 20px;
  }
}
</style>
