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

interface State {
  query: string
  messages: Message[]
  isLoading: boolean
}

export const useQAStore = defineStore('qa', {
  state: (): State => ({
    query: '',
    messages: [],
    isLoading: false
  }),

  actions: {
    setQuery(query: string) {
      this.query = query
    },

    async sendQuery() {
      if (!this.query.trim()) return

      this.isLoading = true

      // Add user message to the messages array
      this.messages.push({ role: 'user', content: this.query })
      const q = this.query;
      this.query = '';
      try {
        const { public: { redlmApiBase } } = useRuntimeConfig()
        const response = await axios.post(`${redlmApiBase}/q-and-a`, {
          query: q
        })

        // Add assistant message to the messages array
        this.messages.push({ role: 'assistant', content: response.data.response, metadata: response.data.metadata })
      } catch (error) {
        console.error('Error sending query:', error)
        // Optionally, you can add an error message to the messages array
        this.messages.push({ role: 'assistant', content: 'Sorry, an error occurred.' })
      } finally {
        this.isLoading = false
        this.query = '' // Reset query after sending
      }
    }
  }
})