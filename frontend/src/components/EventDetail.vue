<script setup>
defineProps({
  event: {
    type: Object,
    default: null,
  },
  loading: {
    type: Boolean,
    default: false,
  },
});

function formatDate(value) {
  return new Date(value).toLocaleString();
}

function formatMetadata(value) {
  return JSON.stringify(value || {}, null, 2);
}
</script>

<template>
  <section class="panel detail-panel">
    <div class="panel-header">
      <div>
        <p class="eyebrow">Detail</p>
        <h2>Selected event</h2>
      </div>
    </div>

    <div v-if="loading" class="empty-state">Loading event detail...</div>
    <div v-else-if="!event" class="empty-state">Select an event to inspect its payload.</div>
    <div v-else class="detail-grid">
      <div class="detail-item">
        <span>ID</span>
        <strong>{{ event.id }}</strong>
      </div>
      <div class="detail-item">
        <span>Service</span>
        <strong>{{ event.service_name }}</strong>
      </div>
      <div class="detail-item">
        <span>Severity</span>
        <strong>{{ event.severity }}</strong>
      </div>
      <div class="detail-item">
        <span>Environment</span>
        <strong>{{ event.environment }}</strong>
      </div>
      <div class="detail-item">
        <span>Status code</span>
        <strong>{{ event.status_code ?? "-" }}</strong>
      </div>
      <div class="detail-item">
        <span>Response time</span>
        <strong>{{ event.response_time_ms ? `${event.response_time_ms} ms` : "-" }}</strong>
      </div>
      <div class="detail-item">
        <span>Created at</span>
        <strong>{{ formatDate(event.created_at) }}</strong>
      </div>
      <div class="detail-item">
        <span>Ingested at</span>
        <strong>{{ formatDate(event.ingested_at) }}</strong>
      </div>
      <div class="detail-item detail-item-full">
        <span>Message</span>
        <strong>{{ event.message }}</strong>
      </div>
      <div class="detail-item detail-item-full">
        <span>Metadata</span>
        <pre>{{ formatMetadata(event.metadata) }}</pre>
      </div>
    </div>
  </section>
</template>

