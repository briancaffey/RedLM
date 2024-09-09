<template>
  <DrawerModified v-bind:open="isOpen">
    <DrawerContent>
      <DrawerHeader>
        <DrawerTitle>Are you absolutely sure?</DrawerTitle>
        <DrawerDescription>This action cannot be undone.</DrawerDescription>
      </DrawerHeader>
      <DrawerFooter>
        <Button>Submit</Button>
        <DrawerClose>
          <Button variant="outline" @click="isOpen = false">Cancel</Button>
        </DrawerClose>
      </DrawerFooter>
    </DrawerContent>
</DrawerModified>
<Button @click="isOpen = true">Open Drawer</Button>

</template>

<script setup lang="ts">
import { ref } from 'vue';
import {
  DrawerModified,
  DrawerClose,
  DrawerContent,
  DrawerDescription,
  DrawerFooter,
  DrawerHeader,
  DrawerTitle,
  DrawerTrigger,
} from "@/components/ui/drawer"

import { Button } from "@/components/ui/button"

const isOpen = ref(false);

</script>

<style scoped>
</style>