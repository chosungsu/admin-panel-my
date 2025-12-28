<template>
  <div class="flex items-center">
    <DropdownMenuRoot>
      <DropdownMenuTrigger as-child>
        <button
          :class="triggerClass"
          class="inline-flex items-center justify-start gap-2 overflow-hidden rounded-lg border border-border bg-card px-3 text-sm text-foreground shadow-soft transition"
        >
          <span v-if="!isCompact" class="flex-1 min-w-0 truncate text-left">
            {{ selectedProject?.name || "Select project" }}
          </span>
          <span v-else class="sr-only">Select project</span>
          <ChevronDown class="ml-auto h-4 w-4 shrink-0 text-muted-foreground" />
        </button>
      </DropdownMenuTrigger>
      <DropdownMenuPortal>
        <DropdownMenuContent :class="contentClass" align="start" side="bottom" :side-offset="8">
          <DropdownMenuItem
            v-for="project in props.projects"
            :key="project.id"
            :class="[
              'flex items-center justify-between rounded-md px-3 py-2 text-sm text-foreground cursor-pointer',
              project.id === props.selectedProjectId ? 'bg-muted' : 'hover:bg-muted'
            ]"
            @select="handleProjectSelect(project.id)"
          >
            <span class="truncate">{{ project.name }}</span>
            <Check v-if="project.id === props.selectedProjectId" class="ml-2 h-4 w-4 text-primary shrink-0" />
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenuPortal>
    </DropdownMenuRoot>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from "vue";
import {
  DropdownMenuRoot,
  DropdownMenuTrigger,
  DropdownMenuPortal,
  DropdownMenuContent,
  DropdownMenuItem,
} from "radix-vue";
import { Check, ChevronDown } from "lucide-vue-next";
import type { Project } from "@/lib/types";

const props = defineProps<{
  projects: Project[];
  selectedProjectId: string;
}>();

const emit = defineEmits<{
  (e: "project-change", value: string): void;
}>();

const isCompact = ref(false);
const isNarrow = ref(false);
const screenWidth = ref(0);

const updateCompact = () => {
  if (typeof window === "undefined") return;
  screenWidth.value = window.innerWidth;
  isCompact.value = window.innerWidth <= 520;
  isNarrow.value = window.innerWidth <= 960;
};

onMounted(() => {
  updateCompact();
  window.addEventListener("resize", updateCompact);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", updateCompact);
});

const selectedProject = computed(() =>
  props.projects.find((project) => project.id === props.selectedProjectId)
);

const triggerClass = computed(() => {
  if (isCompact.value) {
    return "w-10 h-9 justify-center px-2";
  }
  if (isNarrow.value) {
    return "w-[180px] h-9";
  }
  return "w-[240px] h-9";
});

const contentClass = computed(() => {
  if (isCompact.value) {
    return "z-50 w-[200px] rounded-xl border border-border bg-card p-2 shadow-xl";
  }
  if (isNarrow.value) {
    return "z-50 w-[180px] rounded-xl border border-border bg-card p-2 shadow-xl";
  }
  return "z-50 w-[240px] rounded-xl border border-border bg-card p-2 shadow-xl";
});

const handleProjectSelect = (projectId: string) => {
  emit("project-change", projectId);
};
</script>
