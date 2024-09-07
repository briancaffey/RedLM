<template>
  <div class="mx-auto max-w-5xl px-2 sm:px-4 md:px-4 lg:px-16 mt-4">
    <NuxtLink class="p-4" v-for="(chapter, i) in chapters" :to="`/chapter/${i+1}`" loading="lazy">
      <Card class="m-4">
        <CardHeader class="text-center">
          <CardTitle>{{ chapter.title }}</CardTitle>
        </CardHeader>
        <CardContent>
          <NuxtImg :src="`/img/paintings/${chapter.images[0] || '1.png'}`" />
        </CardContent>
      </Card>
    </NuxtLink>
  </div>
</template>

<script setup lang="ts">
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

import { useChapterStore } from '@/stores/chapters';
import { storeToRefs } from 'pinia';

const chapterStore = useChapterStore();
const { chapters } = storeToRefs(chapterStore);
</script>