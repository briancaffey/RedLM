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
    <p>Selected area data URL:</p>
    <textarea v-model="selectedAreaDataUrl" readonly></textarea>
    <div v-if="selectedAreaDataUrl" class="preview">
      <p>Preview:</p>
      <img :src="selectedAreaDataUrl" alt="Selected area preview" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

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
    const maxHeight = window.innerHeight * 0.8; // Use 80% of viewport height
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
    ctx.value.setLineDash([5 / scale.value, 5 / scale.value]);
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
  height: 80vh;
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
