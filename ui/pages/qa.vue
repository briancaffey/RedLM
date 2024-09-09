<template>
<template>
  <div class="flex flex-col max-w-xl mx-auto p-4 space-y-4">
    <div v-for="(message, index) in store.messages" :key="index" class="bg-gray-100 p-2 rounded shadow-sm">
      <p class="text-sm">
        <strong>{{ message.role }}:</strong> {{ message.content }}
      </p>
    </div>

    <div class="flex flex-col space-y-2">
      <textarea
        v-model="store.query"
        @keyup.enter="store.sendQuery"
        placeholder="Type your query..."
        class="border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button
        @click="store.sendQuery"
        :disabled="store.isLoading"
        class="bg-red-700 text-white p-2 rounded disabled:bg-gray-300"
      >
        Send
      </button>
    </div>
  </div>
</template>

</template>

<script setup lang="ts">
import { useQAStore } from '@/stores/qa'

const store = useQAStore()
</script>