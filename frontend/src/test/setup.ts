import { afterEach, vi } from 'vitest';
import '@testing-library/dom';

// Clean up after each test

// Mock localStorage
const localStorageMock = (() => {
  let store: Record<string, string> = {};
  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => {
      store[key] = value.toString();
    },
    removeItem: (key: string) => {
      delete store[key];
    },
    clear: () => {
      store = {};
    },
  };
})();

// Mock Web Speech API
const speechRecognitionMock = {
  start: vi.fn(),
  stop: vi.fn(),
  addEventListener: vi.fn(),
  removeEventListener: vi.fn(),
};

// Set up globals
Object.defineProperty(window, 'localStorage', { value: localStorageMock });
Object.defineProperty(window, 'SpeechRecognition', { value: vi.fn(() => speechRecognitionMock) });
Object.defineProperty(window, 'webkitSpeechRecognition', { value: vi.fn(() => speechRecognitionMock) });

// Mock matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
}); 