<template>
  <div v-if="chapterData">
    <h2  class="text-center text-6xl my-8 font-medium">{{ chapterData.title }}</h2>
    <div class="flex justify-center items-center"><NuxtImg :src="`/img/paintings/${chapter.images[0] || '1.png'}`" /></div>
    <div class="mx-auto max-w-5xl px-2 sm:px-4 md:px-4 lg:px-16 mt-4">
      <div class="flex flex-col items-center justify-center p-4">
        <div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          <nuxt-link v-for="(image, index) in chapter.images" :to="`/paintings/${image.slice(0, -4)}`">
            <NuxtImg
            :key="index"
            :src="`/img/paintings/${image}`"
            :alt="'Image ' + index"
            :width="768"
            :height="250"
            class="object-cover w-full h-250 md:h-300 lg:h-400 xl:h-500"
            />
          </nuxt-link>
        </div>
      </div>
      <div v-for="(paragraph, index) in chapterData.paragraphs" :key="index" class="flex flex-col lg:flex-row lg:space-x-4 space-y-4 lg:space-y-0">
  <p class="py-2 lg:w-1/3">{{ paragraph.original }}</p>
  <p class="py-2 lg:w-1/3">{{ paragraph.chinese }}</p>
  <p class="py-2 lg:w-1/3">{{ paragraph.english }}</p>
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

import { useChapterStore } from '@/stores/chapters';
import { computed } from 'vue';

const chapterStore = useChapterStore();


const route = useRoute()
const chapterData = ref(null)
const chapter = computed(() => chapterStore.getChapterByNumber(route.params.num));

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
