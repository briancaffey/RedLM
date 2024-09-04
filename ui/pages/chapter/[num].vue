<template>
  <div v-if="chapterData">
    <h2  class="text-center text-2xl font-medium">{{ chapterData.title }}</h2>
    <div><NuxtImg src="/img/002.png" quality="60" /></div>
    <div class="mx-auto max-w-5xl px-2 sm:px-4 md:px-4 lg:px-16 mt-4">
      <div v-for="(paragraph, index) in chapterData.paragraphs" :key="index">
        <p class="py-2">{{ paragraph.original }}</p>
      </div>
    </div>
  </div>
  <div v-else>
    <p>Loading...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const chapterData = ref(null)

onMounted(async () => {
  const num = route.params.num
  try {
    const response = await fetch(`/book/${num}.json`)
    if (response.ok) {
      chapterData.value = await response.json()
    } else {
      console.error(`Failed to load chapter ${num}`)
    }
  } catch (error) {
    console.error(`Error loading chapter ${num}:`, error)
  }
})
</script>
