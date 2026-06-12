import React, { useState } from 'react';
import axios from 'axios';

const FileUpload = ({ onUploadComplete }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const formData = new FormData();
      formData.append('file', e.target.elements.file.files[0]);

      const response = await axios.post('http://localhost:8000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.status === 'success') {
        setSuccess('File uploaded successfully!');
        onUploadComplete(response.data);
      } else {
        setError('Upload failed. Please try again.');
      }
    } catch (err) {
      setError(`Error: ${err.response?.data?.detail || err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold mb-4">Upload Workforce Data</h2>
      <p className="text-gray-600 mb-4">
        Upload CSV, Excel, or JSON files containing workforce/process data for analysis
      </p>

      {error && (
        <div className="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 mb-4">
          {error}
        </div>
      )}

      {success && (
        <div className="bg-green-50 border-l-4 border-green-500 text-green-700 p-4 mb-4">
          {success}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select Data File
          </label>
          <input
            type="file"
            name="file"
            accept=".csv,.xlsx,.xls,.json"
            required
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4
                      file:rounded-full file:border-0 file:text-sm file:font-semibold
                      file:bg-violet-50 file:text-violet-700 hover:file:bg-violet-100"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6
                     rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Uploading...' : 'Upload File'}
        </button>
      </form>

      <div className="mt-6 text-xs text-gray-500">
        <p><strong>Supported formats:</strong> CSV, Excel (.xlsx, .xls), JSON</p>
        <p><strong>Max file size:</strong> 10MB</p>
        <p><strong>Expected columns:</strong> Task name, time per task (min), volume, frequency</p>
      </div>
    </div>
  );
};

export default FileUpload;