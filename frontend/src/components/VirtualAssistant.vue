<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center p-4">
    <div class="w-full max-w-2xl bg-white rounded-lg shadow-lg overflow-hidden">
      <div class="p-4 bg-blue-600 text-white flex justify-between items-center">
        <h1 class="text-xl font-bold">Virtual Assistant</h1>
        <button 
          @click="toggleVoiceInput"
          class="p-2 rounded-full hover:bg-blue-700 transition-colors"
          :class="{ 'bg-red-500': isListening }"
          :disabled="isLoading"
        >
          <svg 
            v-if="isListening" 
            class="w-6 h-6" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
          </svg>
          <svg 
            v-else 
            class="w-6 h-6" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
          </svg>
        </button>
      </div>

      <div 
        ref="messagesContainer"
        class="h-96 overflow-y-auto p-4"
      >
        <transition-group name="message" tag="div" class="space-y-6">
          <div 
            v-for="(message, index) in messages" 
            :key="index"
            :class="[
              'p-4 rounded-lg transition-all duration-300 ease-in-out',
              message.type === 'user' 
                ? 'bg-blue-100 ml-auto max-w-xs' 
                : 'bg-gray-100 w-full'
            ]"
          >
            <div v-html="formatMessage(message.content)" class="prose prose-sm max-w-none"></div>
            <p class="text-xs text-gray-500 mt-2">
              {{ formatTime(message.timestamp) }}
            </p>
          </div>
        </transition-group>
        <div v-if="isLoading" class="flex justify-center mt-6">
          <div class="flex space-x-1">
            <div class="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style="animation-delay: 0ms"></div>
            <div class="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style="animation-delay: 150ms"></div>
            <div class="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style="animation-delay: 300ms"></div>
          </div>
        </div>
      </div>

      <div class="p-4 border-t">
        <div class="flex items-center space-x-2">
          <input
            v-model="userInput"
            @keyup.enter="sendMessage"
            :disabled="isLoading"
            class="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
            placeholder="Type your message..."
          />
          <button
            @click="sendMessage"
            :disabled="!userInput.trim() || isLoading"
            class="p-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import axios from 'axios'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

interface Message {
  type: 'user' | 'assistant'
  content: string
  timestamp: Date
}

export default Vue.extend({
  name: 'VirtualAssistant',
  data() {
    return {
      messages: [] as Message[],
      userInput: '',
      isLoading: false,
      isListening: false,
      recognition: null as any,
      sessionId: this.generateSessionId()
    }
  },
  watch: {
    messages: {
      handler() {
        this.$nextTick(() => {
          this.scrollToBottom()
        })
      },
      deep: true
    }
  },
  mounted() {
    this.initializeSpeechRecognition()
    this.setupImageLoading()
    // Configurar marked para renderizar enlaces como HTML
    marked.setOptions({
      breaks: true,
      gfm: true,
      headerIds: false,
      mangle: false
    })
  },
  methods: {
    scrollToBottom() {
      const container = this.$refs.messagesContainer as HTMLElement
      if (container) {
        container.scrollTop = container.scrollHeight
      }
    },
    formatMessage(content: string): string {
      // Convertir markdown a HTML
      const html = marked(content)
      // Sanitizar el HTML
      const cleanHtml = DOMPurify.sanitize(html, {
        ALLOWED_TAGS: ['p', 'br', 'strong', 'em', 'a', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'img'],
        ALLOWED_ATTR: ['href', 'src', 'alt', 'title', 'class', 'target', 'rel'],
        ADD_ATTR: ['target', 'rel']
      })
      
      // Añadir target="_blank" y rel="noopener noreferrer" a todos los enlaces
      const doc = new DOMParser().parseFromString(cleanHtml, 'text/html')
      
      // Convertir enlaces de imágenes de books.toscrape.com a etiquetas img
      const links = doc.getElementsByTagName('a')
      Array.from(links).forEach(link => {
        const href = link.getAttribute('href')

        if (href && href.includes('books.toscrape.com/media')) {
          const img = doc.createElement('img')
          img.setAttribute('src', href)
          img.setAttribute('alt', 'Book cover')
          img.setAttribute('class', 'max-w-[200px] h-auto rounded-lg my-2')
          link.parentNode?.replaceChild(img, link)
        } else {
          link.setAttribute('target', '_blank')
          link.setAttribute('rel', 'noopener noreferrer')
        }
      })
      
      return doc.body.innerHTML
    },
    setupImageLoading() {
      // Observar cambios en el DOM para manejar la carga de imágenes
      const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
          if (mutation.addedNodes) {
            mutation.addedNodes.forEach((node) => {
              if (node instanceof HTMLElement) {
                const images = node.getElementsByTagName('img')
                Array.from(images).forEach((img) => {
                  img.classList.add('opacity-50', 'bg-gray-100')
                  img.onload = () => {
                    img.classList.remove('opacity-50', 'bg-gray-100')
                  }
                  img.onerror = () => {
                    img.classList.remove('opacity-50', 'bg-gray-100')
                    img.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgZmlsbD0iI2YzZjRmNiIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTQiIGZpbGw9IiM2YjcyODAiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj5JbWFnZSBub3QgZm91bmQ8L3RleHQ+PC9zdmc+'
                  }
                })
              }
            })
          }
        })
      })

      observer.observe(document.body, {
        childList: true,
        subtree: true
      })
    },
    initializeSpeechRecognition() {
      const SpeechRecognition = (window as any).SpeechRecognition || 
        (window as any).webkitSpeechRecognition ||
        (window as any).mozSpeechRecognition ||
        (window as any).msSpeechRecognition;

      if (!SpeechRecognition) {
        console.error('Speech recognition not supported in this browser');
        this.messages.push({
          type: 'assistant',
          content: 'Speech recognition is not supported in your browser. Please use Chrome or Edge.',
          timestamp: new Date()
        });
        return;
      }

      this.recognition = new SpeechRecognition();
      this.recognition.continuous = false;
      this.recognition.interimResults = false;
      this.recognition.lang = 'en-US';
      this.recognition.maxAlternatives = 1;

      this.recognition.onstart = () => {
        console.log('Speech recognition started');
        this.messages.push({
          type: 'assistant',
          content: 'Listening... Please speak now.',
          timestamp: new Date()
        });
      };

      this.recognition.onresult = (event: any) => {
        console.log('Speech recognition result:', event.results);
        const transcript = event.results[0][0].transcript;
        this.userInput = transcript;
        this.sendMessage();
      };

      this.recognition.onend = () => {
        console.log('Speech recognition ended');
        this.isListening = false;
      };

      this.recognition.onerror = (event: any) => {
        console.error('Speech recognition error:', event.error);
        this.isListening = false;
        
        let errorMessage = 'Sorry, there was an error with the microphone. ';
        
        switch (event.error) {
          case 'no-speech':
            errorMessage += 'No speech was detected. Please try speaking again.';
            break;
          case 'audio-capture':
            errorMessage += 'Could not capture audio. Please check your microphone settings.';
            break;
          case 'not-allowed':
            errorMessage += 'Microphone access was denied. Please allow microphone access in your browser settings.';
            break;
          case 'aborted':
            errorMessage += 'Speech recognition was aborted. Please try again.';
            break;
          default:
            errorMessage += 'Please try again.';
        }
        
        this.messages.push({
          type: 'assistant',
          content: errorMessage,
          timestamp: new Date()
        });
      };
    },
    toggleVoiceInput() {
      if (!this.recognition) {
        this.messages.push({
          type: 'assistant',
          content: 'Speech recognition is not supported in your browser. Please use Chrome or Edge.',
          timestamp: new Date()
        });
        return;
      }

      if (this.isListening) {
        console.log('Stopping speech recognition');
        this.recognition.stop();
      } else {
        try {
          console.log('Starting speech recognition');
          this.recognition.start();
          this.isListening = true;
        } catch (error) {
          console.error('Error starting speech recognition:', error);
          this.messages.push({
            type: 'assistant',
            content: 'Could not start the microphone. Please check your permissions and try again.',
            timestamp: new Date()
          });
        }
      }
    },
    generateSessionId(): string {
      return 'session_' + Math.random().toString(36).substring(2, 15)
    },
    async sendMessage() {
      if (!this.userInput.trim() || this.isLoading) return

      const userMessage: Message = {
        type: 'user',
        content: this.userInput,
        timestamp: new Date()
      }
      this.messages.push(userMessage)
      this.userInput = '' // Clear input immediately after sending

      this.isLoading = true
      try {
        const response = await axios.post('/webhook-test/ask', {
          chatInput: userMessage.content,
          sessionId: this.sessionId
        })

        const responseData = response.data[0]
        let content = ''
        
        // Handle both string and object responses
        if (typeof responseData.response === 'string') {
          content = responseData.response
        } else if (typeof responseData.output === 'string') {
          content = responseData.output
        } else if (Array.isArray(responseData.response)) {
          content = responseData.response.map(item => item.text).join('\n')
        } else if (Array.isArray(responseData.output)) {
          content = responseData.output.map(item => item.text).join('\n')
        } else {
          content = 'Sorry, I could not process the response.'
        }

        const assistantMessage: Message = {
          type: 'assistant',
          content: content,
          timestamp: new Date()
        }
        this.messages.push(assistantMessage)
      } catch (error) {
        console.error('Error sending message:', error)
        this.messages.push({
          type: 'assistant',
          content: 'Sorry, I encountered an error. Please try again.',
          timestamp: new Date()
        })
      } finally {
        this.isLoading = false
      }
    },
    formatTime(date: Date): string {
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  }
})
</script> 