import api from './api';

/**
 * Fetch the organization chart hierarchy.
 */
export const fetchOrgChart = async () => {
  const response = await api.get('/api/org-chart');
  return response.data;
};
