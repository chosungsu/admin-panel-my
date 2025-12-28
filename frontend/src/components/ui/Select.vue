<template>
  <SelectRoot :model-value="modelValue" @update:model-value="emit('update:modelValue', $event)">
    <SelectTrigger :class="triggerClass">
      <SelectValue
        v-if="!hideValue"
        :placeholder="placeholder"
        class="flex-1 min-w-0 truncate text-left"
      />
      <span v-else class="sr-only">{{ placeholder }}</span>
      <ChevronDown class="ml-auto h-4 w-4 shrink-0 text-muted-foreground" />
    </SelectTrigger>
    <SelectPortal>
      <SelectContent :class="contentClass" position="popper">
        <SelectViewport>
          <SelectItem
            v-for="option in options"
            :key="option.value"
            :value="option.value"
            class="flex items-center justify-between rounded-md px-3 py-2 text-sm text-foreground hover:bg-muted"
          >
            <SelectItemText class="truncate">{{ option.label }}</SelectItemText>
            <SelectItemIndicator>
              <Check class="h-4 w-4 text-primary" />
            </SelectItemIndicator>
          </SelectItem>
        </SelectViewport>
      </SelectContent>
    </SelectPortal>
  </SelectRoot>
</template>

<script setup lang="ts">
import { computed } from "vue";
import {
  SelectRoot,
  SelectTrigger,
  SelectValue,
  SelectPortal,
  SelectContent,
  SelectViewport,
  SelectItem,
  SelectItemText,
  SelectItemIndicator,
} from "radix-vue";
import { Check, ChevronDown } from "lucide-vue-next";
import { cn } from "@/lib/utils";

export type SelectOption = {
  label: string;
  value: string;
};

const props = defineProps<{
  modelValue: string;
  options: SelectOption[];
  placeholder?: string;
  triggerClass?: string;
  contentClass?: string;
  hideValue?: boolean;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: string): void;
}>();

const triggerClass = computed(() =>
  cn(
    "inline-flex h-12 w-full items-center justify-start gap-2 overflow-hidden rounded-lg border border-border bg-card px-3 text-sm text-foreground shadow-soft transition",
    props.triggerClass
  )
);

const contentClass = computed(() =>
  cn(
    "z-50 rounded-xl border border-border bg-card p-2 shadow-xl",
    props.contentClass || "w-72"
  )
);
</script>
