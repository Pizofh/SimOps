<script setup>
const props = defineProps({
  events: {
    type: Array,
    required: true,
  },
});

const severityOrder = ["info", "warning", "error", "timeout", "latency_spike"];

function countBySeverity(severity) {
  return props.events.filter((event) => event.severity === severity).length;
}

function latestEventDate() {
  if (!props.events.length) {
    return "No events loaded";
  }

  return new Date(props.events[0].created_at).toLocaleString();
}
</script>

<template>
  <section class="summary-grid">
    <article class="summary-card">
      <p class="summary-label">Events shown</p>
      <strong class="summary-value">{{ events.length }}</strong>
    </article>
    <article v-for="severity in severityOrder" :key="severity" class="summary-card">
      <p class="summary-label">{{ severity.replace("_", " ") }}</p>
      <strong class="summary-value">{{ countBySeverity(severity) }}</strong>
    </article>
    <article class="summary-card summary-card-wide">
      <p class="summary-label">Latest event</p>
      <strong class="summary-value summary-value-small">{{ latestEventDate() }}</strong>
    </article>
  </section>
</template>

