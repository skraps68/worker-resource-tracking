import React, { useState } from 'react';
import CreationPanel from './components/CreationPanel';
import ViewingPanel from './components/ViewingPanel';
import OpenRecordsPanel from './components/OpenRecordsPanel';
import QueryPanel from './components/QueryPanel';
import ForecastBudgetPanel from './components/ForecastBudgetPanel';
import './App.css';

/**
 * Main App component with tabbed interface
 * Requirements: 5.1
 */
function App() {
  const [activeTab, setActiveTab] = useState('creation');

  return (
    <div className="app">
      <header className="app-header">
        <h1>Worker Resource Tracking System</h1>
        <p className="app-subtitle">Bi-Temporal Resource Management</p>
      </header>

      <nav className="app-nav">
        <button
          className={`nav-tab ${activeTab === 'creation' ? 'active' : ''}`}
          onClick={() => setActiveTab('creation')}
        >
          Create/Update
        </button>
        <button
          className={`nav-tab ${activeTab === 'viewing' ? 'active' : ''}`}
          onClick={() => setActiveTab('viewing')}
        >
          Active Resources
        </button>
        <button
          className={`nav-tab ${activeTab === 'forecast' ? 'active' : ''}`}
          onClick={() => setActiveTab('forecast')}
        >
          Forecast vs Budget
        </button>
        <button
          className={`nav-tab ${activeTab === 'open' ? 'active' : ''}`}
          onClick={() => setActiveTab('open')}
        >
          Open Resource Records
        </button>
        <button
          className={`nav-tab ${activeTab === 'query' ? 'active' : ''}`}
          onClick={() => setActiveTab('query')}
        >
          Query
        </button>
      </nav>

      <main className="app-main">
        <div style={{ display: activeTab === 'creation' ? 'block' : 'none' }}>
          <CreationPanel />
        </div>
        <div style={{ display: activeTab === 'viewing' ? 'block' : 'none' }}>
          <ViewingPanel />
        </div>
        <div style={{ display: activeTab === 'forecast' ? 'block' : 'none' }}>
          <ForecastBudgetPanel />
        </div>
        <div style={{ display: activeTab === 'open' ? 'block' : 'none' }}>
          <OpenRecordsPanel />
        </div>
        <div style={{ display: activeTab === 'query' ? 'block' : 'none' }}>
          <QueryPanel />
        </div>
      </main>

      <footer className="app-footer">
        <p>Worker Resource Tracking System - Bi-Temporal Data Management</p>
      </footer>
    </div>
  );
}

export default App;
