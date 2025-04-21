/// <reference types="vitest" />

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import sendQuery from './api';

describe('API Utilities', () => {
  const originalFetch = globalThis.fetch;

  beforeEach(() => {
    vi.resetAllMocks();
  });

  afterEach(() => {
    globalThis.fetch = originalFetch;
  });

  describe('sendQuery', () => {
    it('should send a query to the API and return the response', async () => {
      const mockResponse = {
        response: 'This is a test response',
        data: { some: 'data' }
      };
      
      // Mock fetch
      globalThis.fetch = vi.fn().mockResolvedValueOnce({
        json: () => Promise.resolve(mockResponse)
      }) as any;
      
      const result = await sendQuery('test query');
      
      expect(globalThis.fetch).toHaveBeenCalledWith('/api/ask.json', expect.objectContaining({
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      }));
      
      expect(result).toEqual(mockResponse);
    });

    it('should handle errors and return an error message', async () => {
      const mockError = new Error('Network error');
      
      // Mock fetch
      globalThis.fetch = vi.fn().mockRejectedValueOnce(mockError) as any;
      
      const result = await sendQuery('test query');
      
      expect(result).toEqual({
        response: 'Sorry, I encountered an error processing your request.',
        error: 'Network error'
      });
    });
  });
}); 