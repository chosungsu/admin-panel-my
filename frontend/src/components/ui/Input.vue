<template>
  <input
    :type="type"
    :value="modelValue"
    :placeholder="placeholder"
    :class="inputClass"
    @input="handleInput"
  />
</template>

<script setup lang="ts">
import { computed } from "vue";
import { cn } from "@/lib/utils";

const props = withDefaults(defineProps<{
  modelValue?: string | number;
  type?: string;
  placeholder?: string;
  class?: string;
}>(), {
  type: "text",
});

const emit = defineEmits<{
  (e: "update:modelValue", value: string): void;
}>();

const inputClass = computed(() =>
  cn(
    "w-full rounded-md border border-border bg-card px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-[var(--color-accent-weak)]",
    props.class
  )
);

const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement;
  emit("update:modelValue", target.value);
};
</script>
