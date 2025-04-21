import { describe, it, expect, vi, beforeEach } from 'vitest';
import axios from 'axios';
import { sendQuery, fetchConversationHistory } from './api';

// Mock axios
vi.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('API Utilities', () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });

  describe('sendQuery', () => {
    it('should send a query to the n8n webhook and return the response', async () => {
      const mockResponse = {
        data: {
          response: 'This is a test response',
          data: { some: 'data' }
        }
      };
      
      mockedAxios.post.mockResolvedValueOnce(mockResponse);
      
      const result = await sendQuery('test query');
      
      expect(mockedAxios.post).toHaveBeenCalledWith('/ask', { query: 'test query' });
      expect(result).toEqual(mockResponse.data);
    });

    it('should handle errors and return an error message', async () => {
      const mockError = new Error('Network error');
      mockedAxios.post.mockRejectedValueOnce(mockError);
      
      const result = await sendQuery('test query');
      
      expect(mockedAxios.post).toHaveBeenCalledWith('/ask', { query: 'test query' });
      expect(result).toEqual({
        response: 'Sorry, I encountered an error processing your request.',
        error: 'Network error'
      });
    });
  });
}); 