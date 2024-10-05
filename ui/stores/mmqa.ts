/**
 * Multi-modal Q&A store
 *
 * stores information about the base64 encoded image to use in the Qwen2-VL query
 * and the query to make to the RAG service, also keeps track of responses in an array
 *
 */

import { defineStore } from 'pinia'
import axios from 'axios'

interface Metadata {
  content: string
  chapter: number
  paragraph: number
}

interface Message {
  role: 'user' | 'assistant'
  content: string
  metadata?: Metadata[]
}

export const useMmqaStore = defineStore('mmqa', {
  state: () => ({
    base64ImageData: '',
    query: '请描述这张图片的内容。',
    messages: [] as Message[],
    isLoading: false
  }),

  actions: {
    async sendRequest(chapterNumber: string) {
      const { public: { redlmApiBase } } = useRuntimeConfig()
      try {
        // Append user message to messages array
        this.messages.push({ role: 'user', content: this.query })
        this.isLoading = true
        // Make API request
        const response = await axios.post(`${redlmApiBase}/mm-q-and-a`, {
          prompt: this.query,
          image: this.base64ImageData,
          chapter: chapterNumber
        })

        // this.isLoading = false

        // Append assistant response to messages array
        this.messages.push({ role: 'assistant', content: response.data.response, metadata: response.data.metadata })

        return response.data
      } catch (error) {
        console.error('Error sending request:', error)
        throw error
      } finally {
        // Reset isLoading regardless of success or failure
        this.isLoading = false
      }
    },

    setBase64ImageData(data: string) {
      this.base64ImageData = data
    },

    setQuery(query: string) {
      this.query = query
    },

    clearMessages() {
      this.messages = []
    }
  }
})