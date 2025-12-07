/**
 * API client for backend communication
 */

const API_BASE_URL = '/api';

/**
 * Helper function to handle API responses
 */
async function handleResponse(response) {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: 'An error occurred' }));
    throw new Error(error.message || `HTTP error! status: ${response.status}`);
  }
  return response.json();
}

/**
 * Create a new worker and associated resource
 */
export async function createWorker(data) {
  const response = await fetch(`${API_BASE_URL}/workers`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  return handleResponse(response);
}

/**
 * Update a resource by creating a new version
 */
export async function updateResource(rid, data) {
  const response = await fetch(`${API_BASE_URL}/resources/${rid}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  return handleResponse(response);
}

/**
 * Get all currently active resources (business date constrained to today)
 */
export async function getActiveResources() {
  const response = await fetch(`${API_BASE_URL}/resources/active`);
  return handleResponse(response);
}

/**
 * Get all open resource records (proc_end = infinity)
 */
export async function getOpenResourceRecords() {
  const response = await fetch(`${API_BASE_URL}/resources/open`);
  return handleResponse(response);
}

/**
 * Execute a bi-temporal as-of query
 */
export async function getAsOfResources(businessDate, processingDatetime = null) {
  const params = new URLSearchParams({ business_date: businessDate });
  if (processingDatetime) {
    params.append('processing_datetime', processingDatetime);
  }
  
  const response = await fetch(`${API_BASE_URL}/resources/as-of?${params}`);
  return handleResponse(response);
}

/**
 * Get all organizations
 */
export async function getOrgs() {
  const response = await fetch(`${API_BASE_URL}/orgs`);
  return handleResponse(response);
}

/**
 * Get all worker types
 */
export async function getWorkerTypes() {
  const response = await fetch(`${API_BASE_URL}/worker-types`);
  return handleResponse(response);
}
