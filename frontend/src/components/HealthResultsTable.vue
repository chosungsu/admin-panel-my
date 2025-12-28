<template>
  <section class="flex flex-col gap-4 rounded-xl border border-border bg-card p-6 shadow-soft">
    <div>
      <h2 class="text-base font-semibold">Logs</h2>
      <p class="text-sm text-muted-foreground">Latest rows from the database.</p>
    </div>
    <div class="overflow-x-auto rounded-lg border border-border">
      <table class="min-w-[520px] w-full text-sm">
        <thead class="bg-muted text-muted-foreground">
          <tr>
            <th class="px-3 py-2 text-left font-medium">Time</th>
            <th class="px-3 py-2 text-left font-medium">Status</th>
            <th class="px-3 py-2 text-left font-medium">Elasticsearch</th>
            <th class="px-3 py-2 text-left font-medium">Latency</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="rows.length === 0">
            <td colspan="4" class="px-3 py-4 text-center text-muted-foreground">No data yet.</td>
          </tr>
          <tr v-for="row in rows" :key="String(row.id)" class="border-t border-border">
            <td class="px-3 py-2">{{ formatDateTime(row.created_at) }}</td>
            <td class="px-3 py-2">{{ String(row.status_text || "--") }}</td>
            <td class="px-3 py-2">{{ String(row.elasticsearch || "--") }}</td>
            <td class="px-3 py-2">{{ row.latency_ms ? `${row.latency_ms}ms` : "--" }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script setup lang="ts">
const props = defineProps<{
  rows: Array<Record<string, unknown>>;
}>();

const formatDateTime = (value: unknown) => {
  if (typeof value !== "string") return "--";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "--";
  return new Intl.DateTimeFormat(undefined, {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  }).format(date);
};
</script>
