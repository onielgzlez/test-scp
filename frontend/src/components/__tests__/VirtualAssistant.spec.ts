import { mount } from '@vue/test-utils'
import VirtualAssistant from '../VirtualAssistant.vue'
import axios from 'axios'

jest.mock('axios')
const mockedAxios = axios as jest.Mocked<typeof axios>

describe('VirtualAssistant', () => {
  it('renders correctly', () => {
    const wrapper = mount(VirtualAssistant)
    expect(wrapper.exists()).toBe(true)
  })

  it('sends message when enter key is pressed', async () => {
    const wrapper = mount(VirtualAssistant)
    const input = wrapper.find('input')
    
    await input.setValue('Hello')
    await input.trigger('keyup.enter')

    expect(wrapper.vm.$data.userInput).toBe('')
  })

  it('handles API error gracefully', async () => {
    mockedAxios.post.mockRejectedValueOnce(new Error('API Error'))
    
    const wrapper = mount(VirtualAssistant)
    const input = wrapper.find('input')
    
    await input.setValue('Hello')
    await input.trigger('keyup.enter')

    await wrapper.vm.$nextTick()
    const messages = wrapper.vm.$data.messages
    expect(messages[messages.length - 1].content).toContain('Sorry, I encountered an error')
  })

  it('formats time correctly', () => {
    const wrapper = mount(VirtualAssistant)
    const date = new Date('2024-01-01T12:00:00')
    const formattedTime = wrapper.vm.formatTime(date)
    
    expect(formattedTime).toMatch(/^\d{2}:\d{2}$/)
  })

  it('toggles voice input', () => {
    const wrapper = mount(VirtualAssistant)
    const button = wrapper.find('.v-btn')
    
    button.trigger('click')
    expect(wrapper.vm.$data.isListening).toBe(true)
    
    button.trigger('click')
    expect(wrapper.vm.$data.isListening).toBe(false)
  })
}) 