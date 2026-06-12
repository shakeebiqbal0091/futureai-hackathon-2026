import React, { useState } from 'react';
import axios from 'axios';
import FileUpload from './components/FileUpload';
import ChatInterface from './components/ChatInterface';
import FTEDashboard from './components/FTEDashboard';
import ReportViewer from './components/ReportViewer';

function App() {
  const [apiData, setApiData] = useState(null);
  const [analysisResults, setAnalysisResults] = useState(null);
  const [reportData, setReportData] = useState(null);

  const handleFileUpload = (data) => {
    setApiData(data);
    console.log('File uploaded:', data);
  };

  const handleAnalysisComplete = (results) => {
    setAnalysisResults(results);
    console.log('Analysis complete:', results);
  };

  const handleReportGenerated = (report) => {
    setReportData(report);
    console.log('Report generated:', report);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-800">
            WorkForce Intelligence Agent
          </h1>
          <p className="mt-2 text-gray-600">
            An agentic AI system that automates workforce analytics, identifies FTE savings,
            and surfaces productivity insights
          </p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid gap-6 md:grid-cols-2">
          {/* File Upload Section */}
          <FileUpload onUploadComplete={handleFileUpload} />

          {/* Chat Interface Section */}
          <ChatInterface
            apiData={apiData}
            onAnalysisComplete={handleAnalysisComplete}
          />

          {/* FTE Dashboard Section */}
          <FTEDashboard
            analysisResults={analysisResults}
          />

          {/* Report Viewer Section */}
          <ReportViewer
            reportData={reportData}
            onReportGenerated={handleReportGenerated}
          />
        </div>
      </main>

      <footer className="bg-white border-t">
        <div className="max-w-7xl mx-auto px-4 py-6 text-center text-gray-500">
          <p>&copy; 2026 WorkForce Intelligence Agent. Built for FutureAI Global Hackathon 2026.</p>
        </div>
      </footer>
    </div>
  );
}

export default App;