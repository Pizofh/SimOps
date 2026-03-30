<script setup>
defineProps({
  events: {
    type: Array,
    required: true,
  },
  selectedEventId: {
    type: String,
    default: "",
  },
  loading: {
    type: Boolean,
    default: false,
  },
});

defineEmits(["select"]);

function formatDate(value) {
  return new Date(value).toLocaleString();
}
</script>

<template>
  <section class="panel table-panel">
    <div class="panel-header">
      <div>
        <p class="eyebrow">Events</p>
        <h2>Recent activity</h2>
      </div>
      <p class="panel-meta">{{ events.length }} items</p>
    </div>

    <div v-if="loading" class="empty-state">Loading events...</div>
    <div v-else-if="!events.length" class="empty-state">No events match the current filters.</div>

    <div v-else class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Created</th>
            <th>Service</th>
            <th>Severity</th>
            <th>Message</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="event in events"
            :key="event.id"
            :class="{ selected: selectedEventId === event.id }"
            @click="$emit('select', event)"
          >
            <td>{{ formatDate(event.created_at) }}</td>
            <td>{{ event.service_name }}</td>
            <td>
              <span class="severity-pill" :data-severity="event.severity">
                {{ event.severity }}
              </span>
            </td>
            <td class="message-cell">{{ event.message }}</td>
            <td>{{ event.status_code ?? "-" }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

