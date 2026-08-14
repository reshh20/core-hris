import api from './api';


export const fetchOrgChart = async () => {
  const response = await api.get('/api/org-chart');
  return response.data;
};
