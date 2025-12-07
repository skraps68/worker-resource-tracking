import React, { useState, useEffect } from 'react';
import { getActiveResources } from '../api/client';
import './ViewingPanel.css';

/**
 * ViewingPanel component for displaying active resources
 * Requirements: 5.5, 5.7
 */
function ViewingPanel() {
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  /**
   * Fetch active resources on component mount
   */
  useEffect(() => {
    fetchActiveResources();
  }, []);

  /**
   * Fetch active resources from the API
   */
  const fetchActiveResources = async () => {
    setLoading(true);
    setError('');
    
    try {
      const data = await getActiveResources();
      setResources(data);
    } catch (err) {
      setError(`Error loading active resources: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Format date for display
   */
  const formatDate = (dateString) => {
    if (!dateString) return '';
    // Check if it's the infinity date
    if (dateString.startsWith('9999')) return '∞';
    return dateString;
  };

  /**
   * Format datetime for display
   */
  const formatDatetime = (datetimeString) => {
    if (!datetimeString) return '';
    // Check if it's the infinity datetime
    if (datetimeString.startsWith('9999')) return '∞';
    return datetimeString;
  };

  return (
    <div className="panel viewing-panel">
      <div className="panel-header">
        <h2>Active Resources {!loading && resources.length > 0 && `(${resources.length})`}</h2>
        <button 
          onClick={fetchActiveResources} 
          className="btn btn-refresh"
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Refresh'}
        </button>
      </div>

      {error && (
        <div className="message message-error">
          {error}
        </div>
      )}

      {loading && !error && (
        <div className="loading">Loading active resources...</div>
      )}

      {!loading && !error && resources.length === 0 && (
        <div className="no-data">No active resources found.</div>
      )}

      {!loading && !error && resources.length > 0 && (
        <div className="table-container">
          <table className="resources-table">
            <thead>
              <tr>
                <th>RID</th>
                <th>Version</th>
                <th>WID</th>
                <th>Name</th>
                <th>Organization</th>
                <th>Type</th>
                <th>Res Start</th>
                <th>Res End</th>
                <th>Proc Start</th>
                <th>Proc End</th>
              </tr>
            </thead>
            <tbody>
              {resources.map((resource, index) => (
                <tr key={`${resource.RID}-${resource.version}-${index}`}>
                  <td>{resource.RID}</td>
                  <td>{resource.version}</td>
                  <td>{resource.WID}</td>
                  <td>{resource.name}</td>
                  <td>{resource.org}</td>
                  <td>{resource.type}</td>
                  <td>{formatDate(resource.res_start)}</td>
                  <td>{formatDate(resource.res_end)}</td>
                  <td>{formatDatetime(resource.proc_start)}</td>
                  <td>{formatDatetime(resource.proc_end)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default ViewingPanel;
