<template>
  <div class="flex items-center justify-center h-full">
    <div class="loader"></div>
  </div>
</template>

<style>
.loader {
  border: 8px solid #f3f3f3; /* Light grey */
  border-top: 8px solid #b91c1c; /* Red */
  border-radius: 50%;
  width: 60px;
  height: 60px;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>