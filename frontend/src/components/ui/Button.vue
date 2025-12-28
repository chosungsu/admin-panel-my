<template>
  <button
    :type="type"
    :class="buttonClass"
    :disabled="disabled"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { resolveButtonClass, type ButtonVariants } from "./buttonVariants";

const props = withDefaults(defineProps<{
  variant?: ButtonVariants["variant"];
  size?: ButtonVariants["size"];
  type?: "button" | "submit" | "reset";
  disabled?: boolean;
  class?: string;
}>(), {
  variant: "default",
  size: "default",
  type: "button",
  disabled: false,
});

const buttonClass = computed(() => resolveButtonClass(props.variant, props.size, props.class));
</script>
