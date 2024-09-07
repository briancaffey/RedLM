<template>
  <div class="min-h-screen flex flex-col">
    <!-- Navigation Bar -->
    <nav class="bg-red-800 text-white">
      <div class="max-w-7xl mx-auto px-2 sm:px-6 lg:px-8">
        <div class="relative flex items-center justify-between h-16">
          <div class="absolute inset-y-0 left-0 flex items-center sm:hidden">
            <!-- Mobile menu button-->
            <button
              type="button"
              class="inline-flex items-center justify-center p-2 rounded-md text-red-400 hover:text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
              aria-controls="mobile-menu"
              aria-expanded="false"
            >
              <span class="sr-only">Open main menu</span>
              <!-- Icon when menu is closed. -->
              <!-- Heroicon name: outline/menu -->
              <svg
                class="block h-6 w-6"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4 6h16M4 12h16M4 18h16"
                />
              </svg>
              <!-- Icon when menu is open. -->
              <!-- Heroicon name: outline/x -->
              <svg
                class="hidden h-6 w-6"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
          <div class="flex-1 flex items-center justify-center sm:items-stretch sm:justify-start">
            <div class="flex-shrink-0">
            </div>
            <div class="hidden sm:block sm:ml-6">
              <div class="flex space-x-4">
                <!-- Navigation links -->
                <nuxt-link to="/" class="bg-red-900 text-white px-3 py-2 rounded-md text-sm font-medium">
                  RedLM
                </nuxt-link>
                <nuxt-link to="/about" class="text-red-300 hover:bg-red-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">
                  About
                </nuxt-link>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Mobile menu, show/hide based on menu state. -->
      <div class="sm:hidden" id="mobile-menu">
        <div class="px-2 pt-2 pb-3 space-y-1">
          <a href="#" class="bg-red-900 text-white block px-3 py-2 rounded-md text-base font-medium">
            RedLM
          </a>
          <a href="#" class="text-red-300 hover:bg-red-700 hover:text-white block px-3 py-2 rounded-md text-base font-medium">
            About
          </a>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="flex-grow bg-red-100 p-4">
      <NuxtPage />
    </main>

    <!-- Footer (optional) -->
    <footer class="bg-red-800 text-white text-center p-4">
      RedLM
    </footer>
  </div>
</template>

<script setup>
</script>

<style scoped>
</style>
