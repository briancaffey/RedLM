<script lang="ts" setup>
import { ref, watch } from 'vue'
import type { DrawerRootEmits, DrawerRootProps } from 'vaul-vue'
import { DrawerRoot, DrawerContent, DrawerOverlay } from 'vaul-vue'
import { useForwardPropsEmits } from 'radix-vue'

interface ExtendedDrawerRootProps extends DrawerRootProps {
  open?: boolean
}

const props = withDefaults(defineProps<ExtendedDrawerRootProps>(), {
  shouldScaleBackground: true,
  open: false,
})

const emits = defineEmits<DrawerRootEmits & {
  (e: 'update:open', value: boolean): void
}>()

const isOpen = ref(props.open)

watch(() => props.open, (newValue) => {
  isOpen.value = newValue
})

const forwarded = useForwardPropsEmits(props, emits)

const onOpenChange = (open: boolean) => {
  isOpen.value = open
  emits('update:open', open)
}

const closeDrawer = () => {
  console.log("closing...")
  isOpen.value = false
  emits('update:open', false)
}
</script>

<template>
  <DrawerRoot v-bind="forwarded" :open="isOpen" @openChange="onOpenChange">
    <DrawerOverlay class="fixed inset-0 bg-red/40" @click="closeDrawer" />
    <DrawerContent>
      <slot />
    </DrawerContent>
  </DrawerRoot>
</template>