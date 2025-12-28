<template>
  <SwitchRoot
    :checked="modelValue"
    @update:checked="emit('update:modelValue', $event)"
    :class="switchRootClass"
  >
    <SwitchThumb :class="switchThumbClass" />
  </SwitchRoot>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { SwitchRoot, SwitchThumb } from "radix-vue";
import { cn } from "@/lib/utils";

const props = withDefaults(defineProps<{
  modelValue: boolean;
  class?: string;
}>(), {
  modelValue: false,
});

const emit = defineEmits<{
  (e: "update:modelValue", value: boolean): void;
}>();

const switchRootClass = computed(() =>
  cn(
    "relative inline-flex h-6 w-11 items-center rounded-full border border-border bg-muted transition-colors data-[state=checked]:bg-primary",
    props.class
  )
);

const switchThumbClass = computed(() =>
  cn(
    "block h-4 w-4 translate-x-1 rounded-full bg-white transition-transform data-[state=checked]:translate-x-6"
  )
);
</script>
