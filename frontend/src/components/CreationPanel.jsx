import React, { useState } from 'react';
import { createWorker, updateResource } from '../api/client';
import './CreationPanel.css';

/**
 * CreationPanel component for creating workers and updating resources
 * Requirements: 5.2, 5.3, 5.4, 5.7
 */
function CreationPanel() {
  // State for worker creation form
  const [workerForm, setWorkerForm] = useState({
    name: '',
    org: '',
    type: '',
    res_start: ''
  });

  // State for resource update form
  const [updateForm, setUpdateForm] = useState({
    rid: '',
    res_start: '',
    res_end: ''
  });

  // State for feedback messages
  const [workerMessage, setWorkerMessage] = useState({ type: '', text: '' });
  const [updateMessage, setUpdateMessage] = useState({ type: '', text: '' });

  // State for loading indicators
  const [workerLoading, setWorkerLoading] = useState(false);
  const [updateLoading, setUpdateLoading] = useState(false);

  /**
   * Handle worker form input changes
   */
  const handleWorkerChange = (e) => {
    const { name, value } = e.target;
    setWorkerForm(prev => ({ ...prev, [name]: value }));
  };

  /**
   * Handle resource update form input changes
   */
  const handleUpdateChange = (e) => {
    const { name, value } = e.target;
    setUpdateForm(prev => ({ ...prev, [name]: value }));
  };

  /**
   * Handle worker creation form submission
   */
  const handleWorkerSubmit = async (e) => {
    e.preventDefault();
    setWorkerLoading(true);
    setWorkerMessage({ type: '', text: '' });

    try {
      const result = await createWorker(workerForm);
      setWorkerMessage({
        type: 'success',
        text: `Worker created successfully! WID: ${result.WID}, RID: ${result.RID}, Version: ${result.version}`
      });
      // Reset form
      setWorkerForm({ name: '', org: '', type: '', res_start: '' });
    } catch (error) {
      setWorkerMessage({
        type: 'error',
        text: `Error: ${error.message}`
      });
    } finally {
      setWorkerLoading(false);
    }
  };

  /**
   * Handle resource update form submission
   */
  const handleUpdateSubmit = async (e) => {
    e.preventDefault();
    setUpdateLoading(true);
    setUpdateMessage({ type: '', text: '' });

    // Validate that at least one date is provided
    if (!updateForm.res_start && !updateForm.res_end) {
      setUpdateMessage({
        type: 'error',
        text: 'At least one of res_start or res_end must be provided'
      });
      setUpdateLoading(false);
      return;
    }

    try {
      const updateData = {};
      if (updateForm.res_start) updateData.res_start = updateForm.res_start;
      if (updateForm.res_end) updateData.res_end = updateForm.res_end;

      const result = await updateResource(updateForm.rid, updateData);
      setUpdateMessage({
        type: 'success',
        text: `Resource updated successfully! RID: ${result.RID}, New Version: ${result.version}`
      });
      // Reset form
      setUpdateForm({ rid: '', res_start: '', res_end: '' });
    } catch (error) {
      setUpdateMessage({
        type: 'error',
        text: `Error: ${error.message}`
      });
    } finally {
      setUpdateLoading(false);
    }
  };

  return (
    <div className="panel creation-panel">
      <h2>Creation Panel</h2>
      
      {/* Worker Creation Form */}
      <section className="form-section">
        <h3>Create New Worker and Resource</h3>
        <form onSubmit={handleWorkerSubmit} className="creation-form">
          <div className="form-group">
            <label htmlFor="name">Name:</label>
            <input
              type="text"
              id="name"
              name="name"
              value={workerForm.name}
              onChange={handleWorkerChange}
              required
              disabled={workerLoading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="org">Organization:</label>
            <input
              type="text"
              id="org"
              name="org"
              value={workerForm.org}
              onChange={handleWorkerChange}
              required
              disabled={workerLoading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="type">Type:</label>
            <input
              type="text"
              id="type"
              name="type"
              value={workerForm.type}
              onChange={handleWorkerChange}
              required
              disabled={workerLoading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="res_start">Resource Start Date:</label>
            <input
              type="date"
              id="res_start"
              name="res_start"
              value={workerForm.res_start}
              onChange={handleWorkerChange}
              required
              disabled={workerLoading}
            />
          </div>

          <button type="submit" className="btn btn-primary" disabled={workerLoading}>
            {workerLoading ? 'Creating...' : 'Create Worker'}
          </button>

          {workerMessage.text && (
            <div className={`message message-${workerMessage.type}`}>
              {workerMessage.text}
            </div>
          )}
        </form>
      </section>

      {/* Resource Update Form */}
      <section className="form-section">
        <h3>Update Existing Resource</h3>
        <form onSubmit={handleUpdateSubmit} className="creation-form">
          <div className="form-group">
            <label htmlFor="rid">Resource ID (RID):</label>
            <input
              type="number"
              id="rid"
              name="rid"
              value={updateForm.rid}
              onChange={handleUpdateChange}
              required
              disabled={updateLoading}
              min="1"
            />
          </div>

          <div className="form-group">
            <label htmlFor="update_res_start">New Resource Start Date (optional):</label>
            <input
              type="date"
              id="update_res_start"
              name="res_start"
              value={updateForm.res_start}
              onChange={handleUpdateChange}
              disabled={updateLoading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="update_res_end">New Resource End Date (optional):</label>
            <input
              type="date"
              id="update_res_end"
              name="res_end"
              value={updateForm.res_end}
              onChange={handleUpdateChange}
              disabled={updateLoading}
            />
          </div>

          <button type="submit" className="btn btn-primary" disabled={updateLoading}>
            {updateLoading ? 'Updating...' : 'Update Resource'}
          </button>

          {updateMessage.text && (
            <div className={`message message-${updateMessage.type}`}>
              {updateMessage.text}
            </div>
          )}
        </form>
      </section>
    </div>
  );
}

export default CreationPanel;
