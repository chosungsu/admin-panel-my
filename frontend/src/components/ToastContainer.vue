<template>
  <div class="fixed bottom-6 left-1/2 z-[9999] flex -translate-x-1/2 flex-col items-center gap-2">
    <div
      v-for="toast in toasts"
      :key="toast.id"
      class="max-w-[420px] rounded-lg px-4 py-3 text-sm font-medium shadow-lg"
      :class="toastClass(toast.type)"
      @click="removeToast(toast.id)"
    >
      {{ toast.message }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { useToast } from "@/composables/useToast";

const { toasts, removeToast } = useToast();

const toastClass = (type: string) => {
  if (type === "success") return "bg-green-500 text-white";
  if (type === "error") return "bg-red-500 text-white";
  return "bg-card text-foreground border border-border";
};
</script>
