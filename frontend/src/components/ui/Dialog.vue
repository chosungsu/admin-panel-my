<template>
  <DialogRoot :open="open" @update:open="emit('update:open', $event)">
    <DialogPortal>
      <DialogOverlay class="fixed inset-0 bg-black/50" />
      <DialogContent
        :class="dialogClass"
      >
        <slot />
      </DialogContent>
    </DialogPortal>
  </DialogRoot>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { DialogRoot, DialogPortal, DialogOverlay, DialogContent } from "radix-vue";
import { cn } from "@/lib/utils";

const props = defineProps<{
  open: boolean;
  class?: string;
}>();

const emit = defineEmits<{
  (e: "update:open", value: boolean): void;
}>();

const dialogClass = computed(() =>
  cn(
    "fixed left-1/2 top-1/2 z-50 w-[min(380px,90vw)] -translate-x-1/2 -translate-y-1/2 rounded-xl border border-border bg-card p-6 text-foreground shadow-soft",
    props.class
  )
);
</script>
