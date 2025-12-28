import { reactive, toRefs } from "vue";

export type ToastType = "success" | "error" | "info";

export type Toast = {
  id: string;
  message: string;
  type: ToastType;
};

const state = reactive({
  toasts: [] as Toast[],
});

export function showToast(message: string, type: ToastType = "info") {
  const id = `${Date.now()}-${Math.random()}`;
  state.toasts.push({ id, message, type });
  window.setTimeout(() => {
    removeToast(id);
  }, 2000);
}

export function removeToast(id: string) {
  const index = state.toasts.findIndex((toast) => toast.id === id);
  if (index >= 0) {
    state.toasts.splice(index, 1);
  }
}

export function useToast() {
  return {
    ...toRefs(state),
    showToast,
    removeToast,
  };
}
