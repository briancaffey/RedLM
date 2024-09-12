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
    messages: [] as Message[]
  }),

  actions: {
    async sendRequest(chapterNumber: string) {
      try {
        // Append user message to messages array
        this.messages.push({ role: 'user', content: this.query })

        // Make API request
        const response = await axios.post('http://localhost:8080/mm-q-and-a', {
          prompt: this.query,
          image: this.base64ImageData,
          chapter: chapterNumber
        })

        // Append assistant response to messages array
        this.messages.push({ role: 'assistant', content: response.data.response, metadata: response.data.metadata })

        return response.data
      } catch (error) {
        console.error('Error sending request:', error)
        throw error
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