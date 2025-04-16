<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center p-4">
    <div class="w-full max-w-2xl bg-white rounded-lg shadow-lg overflow-hidden">
      <div class="p-4 bg-blue-600 text-white flex justify-between items-center">
        <h1 class="text-xl font-bold">Virtual Assistant</h1>
        <button 
          @click="toggleVoiceInput"
          class="p-2 rounded-full hover:bg-blue-700 transition-colors"
          :class="{ 'bg-red-500': isListening }"
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

      <div class="h-96 overflow-y-auto p-4 space-y-4">
        <div 
          v-for="(message, index) in messages" 
          :key="index"
          :class="[
            'p-3 rounded-lg max-w-xs',
            message.type === 'user' 
              ? 'bg-blue-100 ml-auto' 
              : 'bg-gray-100'
          ]"
        >
          <p class="text-gray-800">{{ message.content }}</p>
          <p class="text-xs text-gray-500 mt-1">
            {{ formatTime(message.timestamp) }}
          </p>
        </div>
      </div>

      <div class="p-4 border-t">
        <div class="flex items-center space-x-2">
          <input
            v-model="userInput"
            @keyup.enter="sendMessage"
            :disabled="isLoading"
            class="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Type your message..."
          />
          <button
            @click="sendMessage"
            :disabled="!userInput.trim() || isLoading"
            class="p-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
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
      recognition: null as any
    }
  },
  mounted() {
    this.initializeSpeechRecognition()
  },
  methods: {
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
    async sendMessage() {
      if (!this.userInput.trim()) return

      const userMessage: Message = {
        type: 'user',
        content: this.userInput,
        timestamp: new Date()
      }
      this.messages.push(userMessage)

      this.isLoading = true
      try {
        const response = await axios.get('/webhook-test/ask', {
          params: {
            query: this.userInput
          }
        })

        const assistantMessage: Message = {
          type: 'assistant',
          content: response.data.response,
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
        this.userInput = ''
      }
    },
    formatTime(date: Date): string {
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  }
})
</script> 