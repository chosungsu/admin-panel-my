<template>
  <section class="flex flex-col gap-4 rounded-xl border border-border bg-card p-6 shadow-soft">
    <div>
      <h2 class="text-base font-semibold">Delete Results</h2>
      <p class="hidden text-sm text-muted-foreground md:block">
        Remove all health results for this project.
      </p>
    </div>
    <div class="space-y-3">
      <div class="text-sm text-foreground">Project: <strong>{{ projectName }}</strong></div>
      <Button variant="dangerGradient" class="w-full" @click="isConfirmOpen = true">Delete</Button>
      <div v-if="error" class="text-xs text-[var(--color-danger-text)]">{{ error }}</div>
      <div v-if="success" class="text-xs text-green-500">Deleted.</div>
    </div>
  </section>

  <Dialog v-model:open="isConfirmOpen">
    <div class="space-y-4">
      <div>
        <h3 class="text-base font-semibold">Confirm delete</h3>
        <p class="text-sm text-muted-foreground">This will delete all health results for this project. Continue?</p>
      </div>
      <div class="flex justify-end gap-2">
        <Button variant="outline" @click="isConfirmOpen = false" :disabled="isDeleting">Cancel</Button>
        <Button variant="dangerGradient" @click="handleDelete" :disabled="isDeleting">
          {{ isDeleting ? "Deleting..." : "Confirm" }}
        </Button>
      </div>
    </div>
  </Dialog>
</template>

<script setup lang="ts">
import { ref } from "vue";
import Button from "@/components/ui/Button.vue";
import Dialog from "@/components/ui/Dialog.vue";

const props = defineProps<{
  projectName: string;
  onDelete: () => Promise<void> | void;
}>();

const isDeleting = ref(false);
const isConfirmOpen = ref(false);
const error = ref("");
const success = ref(false);

const handleDelete = async () => {
  isDeleting.value = true;
  error.value = "";
  try {
    await props.onDelete();
    success.value = true;
    window.setTimeout(() => {
      success.value = false;
    }, 2000);
  } catch (err) {
    error.value = "Delete failed.";
  } finally {
    isDeleting.value = false;
    isConfirmOpen.value = false;
  }
};
</script>
