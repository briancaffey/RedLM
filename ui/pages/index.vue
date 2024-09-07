<template>
  <div class="mx-auto max-w-5xl px-2 sm:px-4 md:px-4 lg:px-16 mt-4">
    <NuxtLink v-for="(chapter, i) in chapters" :to="`/chapter/${i+1}`">
      <Card>
        <CardHeader>
          <CardTitle>{{ chapter.title }}</CardTitle>
        </CardHeader>
        <CardContent>
          <NuxtImg :src="`/img/paintings/00${i+1}.png`" />
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