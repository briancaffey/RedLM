<template>
  <div class="image-selector">
    <canvas
      ref="canvas"
      @mousedown="startSelection"
      @mousemove="updateSelection"
      @mouseup="endSelection"
      @mouseleave="endSelection"
    ></canvas>
    <p>Selected area data URL:</p>
    <textarea v-model="selectedAreaDataUrl" readonly></textarea>
    <div v-if="selectedAreaDataUrl" class="preview">
      <p>Preview:</p>
      <img :src="selectedAreaDataUrl" alt="Selected area preview" />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';

export default {
  name: 'ImageSelector',
  setup() {
    const canvas = ref(null);
    const ctx = ref(null);
    const image = ref(null);
    const isSelecting = ref(false);
    const selectionStart = ref({ x: 0, y: 0 });
    const selectionEnd = ref({ x: 0, y: 0 });
    const selectedAreaDataUrl = ref('');

    const loadImage = () => {
      image.value = new Image();
      image.value.src = '/img/009.png'; // Replace with your image path
      image.value.onload = () => {
        canvas.value.width = image.value.width;
        canvas.value.height = image.value.height;
        ctx.value.drawImage(image.value, 0, 0);
      };
    };

    const startSelection = (event) => {
      isSelecting.value = true;
      const rect = canvas.value.getBoundingClientRect();
      selectionStart.value = {
        x: event.clientX - rect.left,
        y: event.clientY - rect.top
      };
      selectionEnd.value = { ...selectionStart.value };
    };

    const updateSelection = (event) => {
      if (!isSelecting.value) return;
      const rect = canvas.value.getBoundingClientRect();
      selectionEnd.value = {
        x: event.clientX - rect.left,
        y: event.clientY - rect.top
      };
      drawImageWithSelection();
    };

    const endSelection = () => {
      if (!isSelecting.value) return;
      isSelecting.value = false;
      updateSelectedAreaDataUrl();
    };

    const drawImageWithSelection = () => {
      ctx.value.clearRect(0, 0, canvas.value.width, canvas.value.height);
      ctx.value.drawImage(image.value, 0, 0);

      const width = selectionEnd.value.x - selectionStart.value.x;
      const height = selectionEnd.value.y - selectionStart.value.y;

      ctx.value.strokeStyle = 'red';
      ctx.value.lineWidth = 2;
      ctx.value.setLineDash([5, 5]);
      ctx.value.strokeRect(selectionStart.value.x, selectionStart.value.y, width, height);
    };

    const updateSelectedAreaDataUrl = () => {
      const tempCanvas = document.createElement('canvas');
      const tempCtx = tempCanvas.getContext('2d');
      const width = Math.abs(selectionEnd.value.x - selectionStart.value.x);
      const height = Math.abs(selectionEnd.value.y - selectionStart.value.y);
      const startX = Math.min(selectionStart.value.x, selectionEnd.value.x);
      const startY = Math.min(selectionStart.value.y, selectionEnd.value.y);

      tempCanvas.width = width;
      tempCanvas.height = height;
      tempCtx.drawImage(
        canvas.value,
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
    };

    onMounted(() => {
      ctx.value = canvas.value.getContext('2d');
      loadImage();
    });

    return {
      canvas,
      selectedAreaDataUrl,
      startSelection,
      updateSelection,
      endSelection,
    };
  },
};
</script>

<style scoped>
.image-selector {
  display: flex;
  flex-direction: column;
  align-items: center;
}

canvas {
  border: 1px solid #ccc;
  margin-bottom: 1rem;
}

textarea {
  width: 100%;
  height: 5rem;
  margin-bottom: 1rem;
}

.preview {
  margin-top: 1rem;
}

.preview img {
  max-width: 100%;
  border: 1px solid #ccc;
}
</style>