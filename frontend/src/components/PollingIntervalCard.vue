<template>
  <section class="flex flex-col gap-4 rounded-xl border border-border bg-card p-6 shadow-soft">
    <div>
      <h2 class="text-base font-semibold">Polling Interval</h2>
      <p class="desc text-sm text-muted-foreground">
        Saved per project and used for auto refresh.
      </p>
    </div>
    <div class="space-y-3">
      <label class="text-xs uppercase tracking-[0.08em] text-muted-foreground">Interval (seconds)</label>
      <div class="flex flex-col gap-2 sm:flex-row sm:items-center">
        <Input v-model="inputValue" type="number" :placeholder="String(MIN_SECONDS)" class="sm:flex-1" />
        <Button
          variant="gradient"
          :disabled="isSaving"
          class="sm:w-auto"
          @click="handleSave"
        >
          {{ isSaving ? "Saving..." : "Save" }}
        </Button>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import Input from "@/components/ui/Input.vue";
import Button from "@/components/ui/Button.vue";
import { useToast } from "@/composables/useToast";

const props = defineProps<{
  currentIntervalMs: number;
  onUpdate: (intervalMs: number) => Promise<void> | void;
}>();

const { showToast } = useToast();

const MIN_SECONDS = 5;
const MAX_SECONDS = 3600;

const inputValue = ref("");
const isSaving = ref(false);

const syncInput = () => {
  inputValue.value = String(Math.round(props.currentIntervalMs / 1000));
};

onMounted(syncInput);
watch(() => props.currentIntervalMs, syncInput);

const handleSave = async () => {
  const seconds = Number.parseInt(inputValue.value, 10);
  if (Number.isNaN(seconds)) {
    showToast("Enter a number of seconds.", "error");
    return;
  }
  if (seconds < MIN_SECONDS) {
    showToast(`Minimum is ${MIN_SECONDS}s.`, "error");
    return;
  }
  if (seconds > MAX_SECONDS) {
    showToast(`Maximum is ${MAX_SECONDS}s.`, "error");
    return;
  }

  isSaving.value = true;
  try {
    await props.onUpdate(seconds * 1000);
    showToast("Saved.", "success");
  } catch (err) {
    showToast("Failed to save interval.", "error");
  } finally {
    isSaving.value = false;
  }
};
</script>

<style scoped>
@media (min-width: 770px) and (max-width: 800px) {
  .desc {
    display: none;
  }
}
</style>
