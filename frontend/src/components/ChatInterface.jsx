import React, { useState } from 'react';
import axios from 'axios';

const ChatInterface = ({ apiData, onAnalysisComplete }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');

  const sendMessage = async () => {
    if (!inputValue.trim() || !apiData || loading) return;

    const userMessage = inputValue.trim();

    setLoading(true);
    setError(null);

    // Add user message immediately
    setMessages((prev) => [
      ...prev,
      {
        text: userMessage,
        isUser: true,
      },
    ]);

    setInputValue('');

    try {
      const response = await axios.post('http://localhost:8000/query', {
        query: userMessage,
      });

      if (response.data?.status === 'success') {
        const botMessage = {
          text: response.data.response,
          isUser: false,
          queryType: response.data.query_type,
        };

        // Add bot response without overwriting previous messages
        setMessages((prev) => [...prev, botMessage]);

        // Simulated FTE analysis trigger
        if (
          userMessage.toLowerCase().includes('analyze') ||
          userMessage.toLowerCase().includes('fte') ||
          userMessage.toLowerCase().includes('savings')
        ) {
          setTimeout(() => {
            onAnalysisComplete?.({
              daily_time_saved_hours: 25.5,
              annual_time_saved_hours: 6375,
              fte_equivalent: 3.2,
              annual_cost_savings: 318750,
              automation_opportunities: [
                {
                  task_column: 'Data Entry',
                  annual_time_savings: 2000,
                },
                {
                  task_column: 'Report Generation',
                  annual_time_savings: 1500,
                },
                {
                  task_column: 'File Processing',
                  annual_time_savings: 1000,
                },
              ],
            });
          }, 1000);
        }
      } else {
        setError('Failed to process query. Please try again.');
      }
    } catch (err) {
      setError(
        `Error: ${
          err.response?.data?.detail ||
          err.response?.data?.message ||
          err.message
        }`
      );
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold mb-4">
        Chat with WFIA Agent
      </h2>

      <p className="text-gray-600 mb-4">
        Ask questions about your workforce data or request analysis
      </p>

      {error && (
        <div className="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 mb-4">
          {error}
        </div>
      )}

      <div className="h-96 overflow-y-auto mb-4 bg-gray-50 rounded-lg p-4">
        {messages.length === 0 ? (
          <div className="text-gray-500 text-center py-8">
            <p>Start by uploading data, then ask questions like:</p>

            <div className="mt-3 space-y-2">
              <p>"What insights can you see in the data?"</p>
              <p>"Show me FTE savings analysis"</p>
              <p>"What are the top automation opportunities?"</p>
            </div>
          </div>
        ) : (
          <div className="space-y-3">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`flex ${
                  msg.isUser
                    ? 'justify-end'
                    : 'justify-start'
                }`}
              >
                <div
                  className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg break-words ${
                    msg.isUser
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-200 text-gray-800'
                  }`}
                >
                  <p>{msg.text}</p>

                  {!msg.isUser && msg.queryType && (
                    <span className="block text-xs text-gray-500 mt-1">
                      Query type: {msg.queryType}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="flex space-x-2">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask about your data or request analysis..."
          className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <button
          onClick={sendMessage}
          disabled={loading || !inputValue.trim() || !apiData}
          className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Sending...' : 'Send'}
        </button>
      </div>

      {!apiData && (
        <div className="mt-4 text-sm text-gray-500">
          <p>
            Please upload data first to enable chat functionality.
          </p>
        </div>
      )}
    </div>
  );
};

export default ChatInterface;