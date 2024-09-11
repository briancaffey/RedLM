<template>
  <div class="flex flex-col w-xl max-w-xl mx-auto space-y-4">
    <div class="text-center text-3xl">问答</div>
    <div v-for="(message, index) in store.messages" :key="index" :class="[ message.role === 'assistant' ? ' self-start' : 'self-end', 'rounded']">
        <div>
          <p :class="[
            message.role === 'assistant'
            ? 'bg-red-700 text-white self-start text-left'
            : 'bg-white self-end text-right',
            'max-w-md p-4 rounded-lg'
          ]">
          {{ message.content }}
        </p>
      </div>
    </div>

    <div class="flex flex-col space-y-2">
      <textarea
        v-model="store.query"
        @keyup.enter="store.sendQuery"
        placeholder="写下汝之疑问"
        class="border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button
        @click="store.sendQuery"
        :disabled="store.isLoading"
        class="bg-red-700 text-white p-2 rounded disabled:bg-gray-300"
      >
      问话
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useQAStore } from '@/stores/qa'

const store = useQAStore()
</script>