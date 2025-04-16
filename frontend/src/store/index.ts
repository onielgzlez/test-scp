import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    conversationHistory: [] as Array<{
      type: 'user' | 'assistant'
      content: string
      timestamp: Date
    }>
  },
  mutations: {
    addMessage(state, message) {
      state.conversationHistory.push(message)
    }
  },
  actions: {
    addMessage({ commit }, message) {
      commit('addMessage', message)
    }
  },
  getters: {
    getConversationHistory: state => state.conversationHistory
  }
}) 