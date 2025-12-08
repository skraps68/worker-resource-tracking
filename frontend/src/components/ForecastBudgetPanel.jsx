import React, { useState, useEffect } from 'react';
import { getForecastBudgetData, getOrgs } from '../api/client';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './ForecastBudgetPanel.css';

/**
 * ForecastBudgetPanel component for displaying forecast vs budget time series
 */
function ForecastBudgetPanel() {
  const [selectedOrg, setSelectedOrg] = useState('All');
  const [orgs, setOrgs] = useState([]);
  const [chartData, setChartData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  /**
   * Fetch organizations on component mount
   */
  useEffect(() => {
    fetchOrgs();
  }, []);

  /**
   * Fetch chart data when selected org changes
   */
  useEffect(() => {
    if (selectedOrg) {
      fetchChartData(selectedOrg);
    }
  }, [selectedOrg]);

  /**
   * Fetch organizations for dropdown
   */
  const fetchOrgs = async () => {
    try {
      const data = await getOrgs();
      setOrgs(data);
      
      // Find root org (org with no parent) and set as default
      const rootOrg = data.find(org => org.parent === null);
      if (rootOrg) {
        setSelectedOrg(rootOrg.name);
      }
    } catch (err) {
      setError(`Error loading organizations: ${err.message}`);
    }
  };

  /**
   * Fetch forecast and budget data for selected org
   */
  const fetchChartData = async (orgName) => {
    setLoading(true);
    setError('');
    
    try {
      const data = await getForecastBudgetData(orgName);
      
      // Merge budget and forecast data by date
      const dateMap = new Map();
      
      data.budget.forEach(item => {
        dateMap.set(item.date, { date: item.date, budget: item.value });
      });
      
      data.forecast.forEach(item => {
        if (dateMap.has(item.date)) {
          dateMap.get(item.date).forecast = item.value;
        } else {
          dateMap.set(item.date, { date: item.date, forecast: item.value });
        }
      });
      
      // Convert to array and sort by date
      const mergedData = Array.from(dateMap.values()).sort((a, b) => 
        new Date(a.date) - new Date(b.date)
      );
      
      setChartData(mergedData);
    } catch (err) {
      setError(`Error loading chart data: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Handle org selection change
   */
  const handleOrgChange = (e) => {
    setSelectedOrg(e.target.value);
  };

  return (
    <div className="panel forecast-budget-panel">
      <div className="panel-header">
        <h2>Forecast vs Budget</h2>
        <div className="org-selector">
          <label htmlFor="org-select">Organization:</label>
          <select
            id="org-select"
            value={selectedOrg}
            onChange={handleOrgChange}
            disabled={loading}
          >
            {orgs.map((org) => (
              <option key={org.name} value={org.name}>
                {org.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {error && (
        <div className="message message-error">
          {error}
        </div>
      )}

      {loading && !error && (
        <div className="loading">Loading chart data...</div>
      )}

      {!loading && !error && chartData.length === 0 && (
        <div className="no-data">No forecast or budget data available for this organization.</div>
      )}

      {!loading && !error && chartData.length > 0 && (
        <div className="chart-container">
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="date" 
                label={{ value: 'Date', position: 'insideBottom', offset: -5 }}
              />
              <YAxis 
                label={{ value: 'Headcount', angle: -90, position: 'insideLeft' }}
              />
              <Tooltip />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="budget" 
                stroke="#2196F3" 
                strokeWidth={2}
                name="Budget"
                connectNulls
              />
              <Line 
                type="monotone" 
                dataKey="forecast" 
                stroke="#4CAF50" 
                strokeWidth={2}
                name="Forecast"
                connectNulls
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}

export default ForecastBudgetPanel;
