<template>
  <div class="flex flex-col w-xl max-w-xl mx-auto space-y-4">
    <div class="text-center text-3xl">问答</div>
    <div
      v-for="(message, index) in store.messages"
      :key="index"
      :class="[ message.role === 'assistant' ? ' self-start' : 'self-end', 'rounded'
      ]">
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
      <TooltipProvider>
        <Tooltip v-for="(metadata, index) in message.metadata">
          <TooltipTrigger asChild>
            <NuxtLink :to="`/chapter/${metadata.chapter}#${metadata.paragraph}`">
              <Badge class="bg-emerald-700 hover:bg-emerald-800 mr-2 mt-2 px-4 py-2 text-base">第 {{ metadata.chapter }} 回； 第 {{ metadata.paragraph + 1 }} 段落</Badge>
            </NuxtLink>
          </TooltipTrigger>
          <TooltipContent class="max-w-60">
            {{ metadata.content }}
          </TooltipContent>
        </Tooltip>
      </TooltipProvider>
    </div>
    <LoadingSpinner class="justify-center" v-if="store.isLoading" />

    <div class="flex flex-col space-y-2">
      <textarea
        v-model="store.query"
        @keyup.enter="askQuestion"
        placeholder="写下汝之疑问"
        class="border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button
        @click="askQuestion"
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
import { Badge } from '@/components/ui/badge'
import { Tooltip, TooltipTrigger, TooltipContent, TooltipProvider } from '@/components/ui/tooltip'

const store = useQAStore()

const askQuestion = async () => {
  await store.sendQuery();
  window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
}
</script>