import React, { useState } from 'react';
import CreationPanel from './components/CreationPanel';
import ViewingPanel from './components/ViewingPanel';
import QueryPanel from './components/QueryPanel';
import './App.css';

/**
 * Main App component with tabbed interface
 * Requirements: 5.1
 */
function App() {
  const [activeTab, setActiveTab] = useState('creation');

  /**
   * Render the active panel based on selected tab
   */
  const renderActivePanel = () => {
    switch (activeTab) {
      case 'creation':
        return <CreationPanel />;
      case 'viewing':
        return <ViewingPanel />;
      case 'query':
        return <QueryPanel />;
      default:
        return <CreationPanel />;
    }
  };

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
          Creation
        </button>
        <button
          className={`nav-tab ${activeTab === 'viewing' ? 'active' : ''}`}
          onClick={() => setActiveTab('viewing')}
        >
          Active Resources
        </button>
        <button
          className={`nav-tab ${activeTab === 'query' ? 'active' : ''}`}
          onClick={() => setActiveTab('query')}
        >
          Query History
        </button>
      </nav>

      <main className="app-main">
        {renderActivePanel()}
      </main>

      <footer className="app-footer">
        <p>Worker Resource Tracking System - Bi-Temporal Data Management</p>
      </footer>
    </div>
  );
}

export default App;
