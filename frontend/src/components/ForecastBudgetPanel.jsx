import React, { useState, useEffect } from 'react';
import { getForecastBudgetData, getOrgs } from '../api/client';
import { ComposedChart, Line, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
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
      
      // Calculate variance for area coloring
      // We need to create stacked areas that fill between the lines
      // When budget > forecast (under budget): green area from forecast to budget
      // When forecast > budget (over budget): red area from budget to forecast
      const dataWithVariance = mergedData.map(item => {
        const isUnderBudget = item.budget >= item.forecast;
        return {
          ...item,
          // Base layer: always the lower value
          baseValue: Math.min(item.budget, item.forecast),
          // Green area: difference when under budget
          underBudgetArea: isUnderBudget ? item.budget - item.forecast : 0,
          // Red area: difference when over budget
          overBudgetArea: !isUnderBudget ? item.forecast - item.budget : 0,
          isUnderBudget
        };
      });
      
      setChartData(dataWithVariance);
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

  /**
   * Custom tooltip to show variance information
   */
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      const variance = data.budget - data.forecast;
      const varianceLabel = variance >= 0 ? 'Under Budget' : 'Over Budget';
      const varianceColor = variance >= 0 ? '#4CAF50' : '#f44336';
      
      return (
        <div className="custom-tooltip">
          <p className="tooltip-date"><strong>{data.date}</strong></p>
          <p className="tooltip-budget">Budget: {data.budget}</p>
          <p className="tooltip-forecast">Forecast: {data.forecast}</p>
          <p className="tooltip-variance" style={{ color: varianceColor }}>
            {varianceLabel}: {Math.abs(variance)}
          </p>
        </div>
      );
    }
    return null;
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
            <ComposedChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <defs>
                <linearGradient id="colorUnderBudget" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#4CAF50" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#4CAF50" stopOpacity={0.1}/>
                </linearGradient>
                <linearGradient id="colorOverBudget" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#f44336" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#f44336" stopOpacity={0.1}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="date" 
                label={{ value: 'Date', position: 'insideBottom', offset: -5 }}
              />
              <YAxis 
                label={{ value: 'Headcount', angle: -90, position: 'insideLeft' }}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend />
              
              {/* Base area (invisible, just to establish baseline) */}
              <Area
                type="monotone"
                dataKey="baseValue"
                fill="transparent"
                stroke="none"
                stackId="variance"
              />
              
              {/* Area for under budget (green) - stacked on base */}
              <Area
                type="monotone"
                dataKey="underBudgetArea"
                fill="url(#colorUnderBudget)"
                stroke="none"
                fillOpacity={1}
                stackId="variance"
                name="Under Budget"
                legendType="none"
              />
              
              {/* Area for over budget (red) - stacked on base */}
              <Area
                type="monotone"
                dataKey="overBudgetArea"
                fill="url(#colorOverBudget)"
                stroke="none"
                fillOpacity={1}
                stackId="variance"
                name="Over Budget"
                legendType="none"
              />
              
              <Line 
                type="monotone" 
                dataKey="budget" 
                stroke="#2196F3" 
                strokeWidth={2}
                name="Budget"
                connectNulls
                dot={{ r: 3 }}
              />
              <Line 
                type="monotone" 
                dataKey="forecast" 
                stroke="#4CAF50" 
                strokeWidth={2}
                name="Forecast"
                connectNulls
                dot={{ r: 3 }}
              />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}

export default ForecastBudgetPanel;
