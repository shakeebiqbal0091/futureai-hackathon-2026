import React from 'react';

const FTEDashboard = ({ analysisResults }) => {
  if (!analysisResults) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4">FTE Savings Analysis</h2>
        <p className="text-gray-600 mb-4">
          Upload data and run analysis to see FTE savings insights here
        </p>
        <div className="text-center py-8">
          <div className="inline-block w-16 h-16 border-4 border-dashed border-gray-300 rounded-full flex items-center justify-center">
            <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m2 0a2 2 0 110-4 2 2 0 010 4zm-6 0a2 2 0 110-4 2 2 0 010 4zm6 0a2 2 0 100-4 2 2 0 000 4z" />
            </svg>
          </div>
          <p className="mt-4">Run analysis from the chat interface</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold mb-4">FTE Savings Analysis</h2>

      {/* Key Metrics */}
      <div className="grid gap-4 md:grid-cols-2 mb-6">
        <div className="bg-blue-50 p-4 rounded-lg">
          <h3 className="text-sm font-medium text-gray-500">Daily Time Saved</h3>
          <p className="text-2xl font-bold text-blue-600">
            {analysisResults.daily_time_saved_hours?.toFixed(1)} hrs
          </p>
        </div>
        <div className="bg-blue-50 p-4 rounded-lg">
          <h3 className="text-sm font-medium text-gray-500">Annual Time Saved</h3>
          <p className="text-2xl font-bold text-blue-600">
            {analysisResults.annual_time_saved_hours?.toLocaleString()} hrs
          </p>
        </div>
        <div className="bg-blue-50 p-4 rounded-lg">
          <h3 className="text-sm font-medium text-gray-500">FTE Equivalent</h3>
          <p className="text-2xl font-bold text-blue-600">
            {analysisResults.fte_equivalent?.toFixed(1)} FTE
          </p>
        </div>
        <div className="bg-blue-50 p-4 rounded-lg">
          <h3 className="text-sm font-medium text-gray-500">Annual Cost Savings</h3>
          <p className="text-2xl font-bold text-blue-600">
            ${analysisResults.annual_cost_savings?.toLocaleString()}
          </p>
        </div>
      </div>

      {/* Automation Opportunities */}
      {analysisResults.automation_opportunities && analysisResults.automation_opportunities.length > 0 && (
        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-4">Top Automation Opportunities</h3>
          <div className="space-y-3">
            {analysisResults.automation_opportunities.map((opp, index) => (
              <div key={index} className="bg-gray-50 p-4 rounded-lg">
                <div className="flex justify-between items-start">
                  <div>
                    <h4 className="font-medium">{opp.task_column || `Task ${index + 1}`}</h4>
                    <p className="text-sm text-gray-500">
                      {opp.annual_time_savings?.toLocaleString()} hours/year
                    </p>
                  </div>
                  <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
                    #{index + 1}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Assumptions */}
      <div className="mt-6 pt-4 border-t border-gray-200">
        <h3 className="text-lg font-semibold mb-4">Calculation Assumptions</h3>
        <div className="text-sm text-gray-600 space-y-1">
          <p>• FTE hours per day: 8 hours</p>
          <p>• Working days per year: 250 days</p>
          <p>• Hourly cost for savings: $50/hour</p>
          <p>• Time savings formula: (time_per_task × volume × frequency) / 60</p>
        </div>
      </div>
    </div>
  );
};

export default FTEDashboard;