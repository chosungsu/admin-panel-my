<template>
  <TooltipProvider :delay-duration="150">
    <TooltipRoot>
      <TooltipTrigger as-child>
        <slot name="trigger" />
      </TooltipTrigger>
      <TooltipContent :side="side" :class="contentClass">
        <slot />
      </TooltipContent>
    </TooltipRoot>
  </TooltipProvider>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { TooltipProvider, TooltipRoot, TooltipTrigger, TooltipContent } from "radix-vue";
import { cn } from "@/lib/utils";

const props = withDefaults(defineProps<{
  side?: "top" | "right" | "bottom" | "left";
  class?: string;
}>(), {
  side: "top",
});

const contentClass = computed(() =>
  cn(
    "z-50 rounded-lg bg-slate-900 px-3 py-2 text-xs text-slate-100 shadow-xl",
    props.class
  )
);
</script>
