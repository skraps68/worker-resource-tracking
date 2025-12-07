import React, { useState, useEffect } from 'react';
import { getOpenResourceRecords } from '../api/client';
import './ViewingPanel.css';

/**
 * OpenRecordsPanel component for displaying open resource records (proc_end = infinity)
 */
function OpenRecordsPanel() {
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  /**
   * Fetch open resource records on component mount
   */
  useEffect(() => {
    fetchOpenRecords();
  }, []);

  /**
   * Fetch open resource records from the API
   */
  const fetchOpenRecords = async () => {
    setLoading(true);
    setError('');
    
    try {
      const data = await getOpenResourceRecords();
      setResources(data);
    } catch (err) {
      setError(`Error loading open resource records: ${err.message}`);
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
        <h2>Open Resource Records {!loading && resources.length > 0 && `(${resources.length})`}</h2>
        <button 
          onClick={fetchOpenRecords} 
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
        <div className="loading">Loading open resource records...</div>
      )}

      {!loading && !error && resources.length === 0 && (
        <div className="no-data">No open resource records found.</div>
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

export default OpenRecordsPanel;
