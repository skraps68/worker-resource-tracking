import React, { useState, useEffect } from 'react';
import { createWorker, updateResource, getActiveResources } from '../api/client';
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
    wid: '',
    name: '',
    org: '',
    res_start: '',
    res_end: '',
    current_res_start: '',
    current_res_end: ''
  });

  // State for active resources (for autocomplete)
  const [activeResources, setActiveResources] = useState([]);
  
  // State for autocomplete suggestions
  const [ridSuggestions, setRidSuggestions] = useState([]);
  const [widSuggestions, setWidSuggestions] = useState([]);
  const [nameSuggestions, setNameSuggestions] = useState([]);
  
  // State for showing/hiding dropdowns
  const [showRidDropdown, setShowRidDropdown] = useState(false);
  const [showWidDropdown, setShowWidDropdown] = useState(false);
  const [showNameDropdown, setShowNameDropdown] = useState(false);

  // State for feedback messages
  const [workerMessage, setWorkerMessage] = useState({ type: '', text: '' });
  const [updateMessage, setUpdateMessage] = useState({ type: '', text: '' });

  // State for loading indicators
  const [workerLoading, setWorkerLoading] = useState(false);
  const [updateLoading, setUpdateLoading] = useState(false);

  /**
   * Fetch active resources on component mount
   */
  useEffect(() => {
    fetchActiveResources();
  }, []);

  /**
   * Fetch active resources for autocomplete
   */
  const fetchActiveResources = async () => {
    try {
      const data = await getActiveResources();
      setActiveResources(data);
    } catch (error) {
      console.error('Error fetching active resources:', error);
    }
  };

  /**
   * Handle worker form input changes
   */
  const handleWorkerChange = (e) => {
    const { name, value } = e.target;
    setWorkerForm(prev => ({ ...prev, [name]: value }));
  };

  /**
   * Handle resource update form input changes with autocomplete
   */
  const handleUpdateChange = (e) => {
    const { name, value } = e.target;
    setUpdateForm(prev => ({ ...prev, [name]: value }));

    // Handle autocomplete for RID
    if (name === 'rid') {
      if (value) {
        const matches = activeResources.filter(r => 
          r.RID.toString().includes(value)
        );
        setRidSuggestions(matches);
        setShowRidDropdown(matches.length > 0);
      } else {
        setRidSuggestions([]);
        setShowRidDropdown(false);
      }
    }

    // Handle autocomplete for WID
    if (name === 'wid') {
      if (value) {
        const matches = activeResources.filter(r => 
          r.WID.toString().includes(value)
        );
        setWidSuggestions(matches);
        setShowWidDropdown(matches.length > 0);
      } else {
        setWidSuggestions([]);
        setShowWidDropdown(false);
      }
    }

    // Handle autocomplete for Name
    if (name === 'name') {
      if (value) {
        const matches = activeResources.filter(r => 
          r.name.toLowerCase().includes(value.toLowerCase())
        );
        setNameSuggestions(matches);
        setShowNameDropdown(matches.length > 0);
      } else {
        setNameSuggestions([]);
        setShowNameDropdown(false);
      }
    }
  };

  /**
   * Handle selection from autocomplete dropdown
   */
  const handleResourceSelect = (resource) => {
    setUpdateForm({
      rid: resource.RID.toString(),
      wid: resource.WID.toString(),
      name: resource.name,
      org: resource.org,
      res_start: '',
      res_end: '',
      current_res_start: resource.res_start,
      current_res_end: resource.res_end
    });
    
    // Hide all dropdowns
    setShowRidDropdown(false);
    setShowWidDropdown(false);
    setShowNameDropdown(false);
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
      <div className="two-column-layout">
        {/* Worker Creation Form */}
        <section className="form-section form-pane">
          <h3>Create Worker/Resource</h3>
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
        <section className="form-section form-pane">
          <h3>Update Resource</h3>
        <form onSubmit={handleUpdateSubmit} className="creation-form">
          <div className="form-row">
            <div className="form-group autocomplete-group">
              <label htmlFor="rid">Resource ID (RID):</label>
              <input
                type="text"
                id="rid"
                name="rid"
                value={updateForm.rid}
                onChange={handleUpdateChange}
                onFocus={() => updateForm.rid && setShowRidDropdown(ridSuggestions.length > 0)}
                onBlur={() => setTimeout(() => setShowRidDropdown(false), 200)}
                required
                disabled={updateLoading}
                placeholder="Type to search..."
                autoComplete="off"
              />
              {showRidDropdown && ridSuggestions.length > 0 && (
                <ul className="autocomplete-dropdown">
                  {ridSuggestions.map((resource) => (
                    <li 
                      key={`rid-${resource.RID}`}
                      onClick={() => handleResourceSelect(resource)}
                    >
                      RID: {resource.RID} - {resource.name} (WID: {resource.WID})
                    </li>
                  ))}
                </ul>
              )}
            </div>

            <div className="form-group autocomplete-group">
              <label htmlFor="wid">Worker ID (WID):</label>
              <input
                type="text"
                id="wid"
                name="wid"
                value={updateForm.wid}
                onChange={handleUpdateChange}
                onFocus={() => updateForm.wid && setShowWidDropdown(widSuggestions.length > 0)}
                onBlur={() => setTimeout(() => setShowWidDropdown(false), 200)}
                disabled={updateLoading}
                placeholder="Type to search..."
                autoComplete="off"
              />
              {showWidDropdown && widSuggestions.length > 0 && (
                <ul className="autocomplete-dropdown">
                  {widSuggestions.map((resource) => (
                    <li 
                      key={`wid-${resource.RID}`}
                      onClick={() => handleResourceSelect(resource)}
                    >
                      WID: {resource.WID} - {resource.name} (RID: {resource.RID})
                    </li>
                  ))}
                </ul>
              )}
            </div>

            <div className="form-group autocomplete-group">
              <label htmlFor="name">Name:</label>
              <input
                type="text"
                id="name"
                name="name"
                value={updateForm.name}
                onChange={handleUpdateChange}
                onFocus={() => updateForm.name && setShowNameDropdown(nameSuggestions.length > 0)}
                onBlur={() => setTimeout(() => setShowNameDropdown(false), 200)}
                disabled={updateLoading}
                placeholder="Type to search..."
                autoComplete="off"
              />
              {showNameDropdown && nameSuggestions.length > 0 && (
                <ul className="autocomplete-dropdown">
                  {nameSuggestions.map((resource) => (
                    <li 
                      key={`name-${resource.RID}`}
                      onClick={() => handleResourceSelect(resource)}
                    >
                      {resource.name} - RID: {resource.RID}, WID: {resource.WID}
                    </li>
                  ))}
                </ul>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="org">Organization:</label>
              <input
                type="text"
                id="org"
                name="org"
                value={updateForm.org}
                disabled
                readOnly
                className="readonly-field"
                placeholder="Auto-filled"
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              {updateForm.current_res_start && (
                <div className="current-date-label">
                  <strong>Current Start Date:</strong> {updateForm.current_res_start}
                </div>
              )}
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
              {updateForm.current_res_end && (
                <div className="current-date-label">
                  <strong>Current End Date:</strong> {updateForm.current_res_end === '9999-12-31' ? '∞' : updateForm.current_res_end}
                </div>
              )}
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
    </div>
  );
}

export default CreationPanel;
