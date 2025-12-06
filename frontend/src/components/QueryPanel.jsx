import React, { useState } from 'react';
import { getAsOfResources } from '../api/client';
import './QueryPanel.css';

/**
 * QueryPanel component for executing bi-temporal as-of queries
 * Requirements: 5.6, 6.1, 5.7
 */
function QueryPanel() {
  const [queryForm, setQueryForm] = useState({
    business_date: '',
    processing_datetime: ''
  });

  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [hasQueried, setHasQueried] = useState(false);

  /**
   * Handle form input changes
   */
  const handleChange = (e) => {
    const { name, value } = e.target;
    setQueryForm(prev => ({ ...prev, [name]: value }));
  };

  /**
   * Handle query form submission
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setHasQueried(true);

    try {
      const data = await getAsOfResources(
        queryForm.business_date,
        queryForm.processing_datetime || null
      );
      setResults(data);
    } catch (err) {
      setError(`Error executing query: ${err.message}`);
      setResults([]);
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
    <div className="panel query-panel">
      <h2>Bi-Temporal As-Of Query</h2>

      <form onSubmit={handleSubmit} className="query-form">
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="business_date">Business Date (required):</label>
            <input
              type="date"
              id="business_date"
              name="business_date"
              value={queryForm.business_date}
              onChange={handleChange}
              required
              disabled={loading}
            />
            <small className="help-text">
              The date for which you want to see resource assignments
            </small>
          </div>

          <div className="form-group">
            <label htmlFor="processing_datetime">Processing Datetime (optional):</label>
            <input
              type="datetime-local"
              id="processing_datetime"
              name="processing_datetime"
              value={queryForm.processing_datetime}
              onChange={handleChange}
              disabled={loading}
            />
            <small className="help-text">
              When the data was recorded (defaults to current time if not specified)
            </small>
          </div>
        </div>

        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Querying...' : 'Execute Query'}
        </button>
      </form>

      {error && (
        <div className="message message-error">
          {error}
        </div>
      )}

      {loading && (
        <div className="loading">Executing query...</div>
      )}

      {!loading && hasQueried && !error && results.length === 0 && (
        <div className="no-data">No resources found for the specified criteria.</div>
      )}

      {!loading && !error && results.length > 0 && (
        <div className="results-section">
          <h3>Query Results ({results.length} resource{results.length !== 1 ? 's' : ''})</h3>
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
                {results.map((resource, index) => (
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
        </div>
      )}
    </div>
  );
}

export default QueryPanel;
