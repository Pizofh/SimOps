<script setup>
import { reactive, watch } from "vue";

const props = defineProps({
  filters: {
    type: Object,
    required: true,
  },
  serviceOptions: {
    type: Array,
    required: true,
  },
  loading: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["update:filters", "refresh"]);

const localFilters = reactive({
  severity: props.filters.severity,
  serviceName: props.filters.serviceName,
  limit: props.filters.limit,
});

watch(
  () => props.filters,
  (value) => {
    localFilters.severity = value.severity;
    localFilters.serviceName = value.serviceName;
    localFilters.limit = value.limit;
  },
  { deep: true },
);

watch(
  localFilters,
  (value) => {
    emit("update:filters", {
      severity: value.severity,
      serviceName: value.serviceName,
      limit: Number(value.limit) || 50,
    });
  },
  { deep: true },
);

function resetFilters() {
  localFilters.severity = "";
  localFilters.serviceName = "";
  localFilters.limit = 50;
}
</script>

<template>
  <section class="panel toolbar-panel">
    <div class="toolbar-header">
      <div>
        <p class="eyebrow">Filters</p>
        <h2>Explore incoming events</h2>
      </div>
      <div class="toolbar-actions">
        <button class="button button-secondary" type="button" @click="resetFilters">Reset</button>
        <button class="button" type="button" :disabled="loading" @click="$emit('refresh')">
          {{ loading ? "Refreshing..." : "Refresh" }}
        </button>
      </div>
    </div>

    <div class="toolbar-grid">
      <label class="field">
        <span>Severity</span>
        <select v-model="localFilters.severity">
          <option value="">All</option>
          <option value="info">info</option>
          <option value="warning">warning</option>
          <option value="error">error</option>
          <option value="timeout">timeout</option>
          <option value="latency_spike">latency_spike</option>
        </select>
      </label>

      <label class="field">
        <span>Service name</span>
        <input
          v-model="localFilters.serviceName"
          list="service-options"
          type="text"
          placeholder="payments-api"
        />
        <datalist id="service-options">
          <option v-for="service in serviceOptions" :key="service" :value="service" />
        </datalist>
      </label>

      <label class="field">
        <span>Limit</span>
        <input v-model.number="localFilters.limit" type="number" min="1" max="200" />
      </label>
    </div>
  </section>
</template>

