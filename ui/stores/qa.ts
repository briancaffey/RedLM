import { defineStore } from 'pinia'
import axios from 'axios'

interface Message {
  role: 'user' | 'assistant'
  content: string
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

      try {
        const response = await axios.post('http://localhost:8080/q-and-a', {
          query: this.query
        })
        console.log("testing..")
        console.log(response);

        // Add assistant message to the messages array
        this.messages.push({ role: 'assistant', content: response.data.response })
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