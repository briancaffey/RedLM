<template>
  <div class="image-selector">
    <div class="canvas-container" ref="canvasContainer">
      <canvas
        ref="canvas"
        @mousedown="startSelection"
        @mousemove="updateSelection"
        @mouseup="endSelection"
        @mouseleave="endSelection"
      ></canvas>
    </div>
    <div v-if="selectedAreaDataUrl" class="preview pt-8">
      <img :src="selectedAreaDataUrl" alt="Selected area preview" />
    </div>
  </div>
    <div class="flex flex-col max-w-xl mx-auto space-y-2">
      <div
        v-for="(message, index) in mmqaStore.messages"
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
      <LoadingSpinner class="justify-center" v-if="mmqaStore.isLoading" />
      <div class="flex flex-col space-y-2">
        <textarea
          v-model="mmqaStore.query"
          class="border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          @click="askQuestion(chapterNum)"
          class="bg-red-700 text-white p-2 rounded disabled:bg-gray-300">
          解图
        </button>
        <button
          @click="mmqaStore.messages = []"
          class="bg-black text-white p-2 rounded disabled:bg-gray-300">
          清除
        </button>
      </div>
    </div>

</template>

<script setup lang="ts">
import { Badge } from '@/components/ui/badge'
import { Tooltip, TooltipTrigger, TooltipContent, TooltipProvider } from '@/components/ui/tooltip'
import { useMmqaStore } from '@/stores/mmqa'
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const mmqaStore = useMmqaStore()
const canvas = ref<HTMLCanvasElement | null>(null);
const canvasContainer = ref<HTMLDivElement | null>(null);
const ctx = ref<CanvasRenderingContext2D | null>(null);
const image = ref<HTMLImageElement | null>(null);
const isSelecting = ref(false);
const selectionStart = ref({ x: 0, y: 0 });
const selectionEnd = ref({ x: 0, y: 0 });
const selectedAreaDataUrl = ref('');
const scale = ref(1);

const route = useRoute();
const imgNum = route.params.num as string;
const chapterNum = route.params.chapter as string;

const loadImage = () => {
  image.value = new Image();
  image.value.src = `/img/paintings/${imgNum}.png`; // Replace with your image path
  image.value.onload = () => {
    calculateScale();
    if (canvas.value) {
      canvas.value.width = image.value.width * scale.value;
      canvas.value.height = image.value.height * scale.value;
    }
    drawImageWithSelection();
  };
};

const calculateScale = () => {
  if (canvasContainer.value && image.value) {
    const maxWidth = canvasContainer.value.clientWidth;
    const maxHeight = window.innerHeight // * 0.8; // Use 80% of viewport height
    const widthScale = maxWidth / image.value.width;
    const heightScale = maxHeight / image.value.height;
    scale.value = Math.min(widthScale, heightScale, 1); // Don't scale up, only down
  }
};

const startSelection = (event: MouseEvent) => {
  if (!canvas.value) return;
  isSelecting.value = true;
  const rect = canvas.value.getBoundingClientRect();
  selectionStart.value = {
    x: (event.clientX - rect.left) / scale.value,
    y: (event.clientY - rect.top) / scale.value
  };
  selectionEnd.value = { ...selectionStart.value };
};

const updateSelection = (event: MouseEvent) => {
  if (!isSelecting.value || !canvas.value) return;
  const rect = canvas.value.getBoundingClientRect();
  selectionEnd.value = {
    x: (event.clientX - rect.left) / scale.value,
    y: (event.clientY - rect.top) / scale.value
  };
  drawImageWithSelection();
};

const endSelection = () => {
  if (!isSelecting.value) return;
  isSelecting.value = false;
  updateSelectedAreaDataUrl();
};

const drawImageWithSelection = () => {
  if (!ctx.value || !canvas.value || !image.value) return;
  ctx.value.clearRect(0, 0, canvas.value.width, canvas.value.height);
  ctx.value.save();
  ctx.value.scale(scale.value, scale.value);
  ctx.value.drawImage(image.value, 0, 0);
  ctx.value.restore();

  if (isSelecting.value) {
    const width = selectionEnd.value.x - selectionStart.value.x;
    const height = selectionEnd.value.y - selectionStart.value.y;

    ctx.value.strokeStyle = 'red';
    ctx.value.lineWidth = 2 / scale.value;
    // ctx.value.setLineDash([5 / scale.value, 5 / scale.value]);
    ctx.value.strokeStyle = 'red';  // Keep the same color
    ctx.value.lineWidth = 4 / scale.value;  // Increase the thickness (adjust the value as needed)

    ctx.value.strokeRect(
      selectionStart.value.x * scale.value,
      selectionStart.value.y * scale.value,
      width * scale.value,
      height * scale.value
    );
  }
};

const updateSelectedAreaDataUrl = () => {
  if (!image.value || !selectionStart.value || !selectionEnd.value) return;
  const tempCanvas = document.createElement('canvas');
  const tempCtx = tempCanvas.getContext('2d');
  const width = Math.abs(selectionEnd.value.x - selectionStart.value.x);
  const height = Math.abs(selectionEnd.value.y - selectionStart.value.y);
  const startX = Math.min(selectionStart.value.x, selectionEnd.value.x);
  const startY = Math.min(selectionStart.value.y, selectionEnd.value.y);

  if (tempCtx) {
    tempCanvas.width = width;
    tempCanvas.height = height;
    tempCtx.drawImage(
      image.value,
      startX,
      startY,
      width,
      height,
      0,
      0,
      width,
      height
    );
    selectedAreaDataUrl.value = tempCanvas.toDataURL();
    mmqaStore.setBase64ImageData(selectedAreaDataUrl.value)
  }
};

onMounted(() => {
  if (canvas.value) {
    ctx.value = canvas.value.getContext('2d');
  }
  loadImage();
  window.addEventListener('resize', () => {
    if (canvas.value && image.value) {
      calculateScale();
      canvas.value.width = image.value.width * scale.value;
      canvas.value.height = image.value.height * scale.value;
      drawImageWithSelection();
    }
  });
});

const askQuestion = async (chapterNumber: string) => {
  await mmqaStore.sendRequest(chapterNumber);
  window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
}
</script>

<style scoped>
.image-selector {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 100vw;
  padding: 1rem;
  box-sizing: border-box;
}

.canvas-container {
  width: 100%;
  /* height: 80vh; */
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

canvas {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

textarea {
  width: 100%;
  height: 5rem;
  margin: 1rem 0;
}

.preview {
  margin-top: 1rem;
  max-width: 100%;
}

.preview img {
  max-width: 500px;
  border: 1px solid #ccc;
}
</style>
