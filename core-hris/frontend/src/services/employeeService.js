import api from './api';

/**
 * Fetch all employees with optional filters.
 */
export const fetchEmployees = async (params = {}) => {
  const response = await api.get('/api/employees', { params });
  return response.data;
};

/**
 * Fetch a single employee by database ID.
 */
export const fetchEmployee = async (id) => {
  const response = await api.get(`/api/employees/${id}`);
  return response.data;
};

/**
 * Fetch all departments.
 */
export const fetchDepartments = async () => {
  const response = await api.get('/api/departments');
  return response.data;
};

/**
 * Fetch all positions.
 */
export const fetchPositions = async () => {
  const response = await api.get('/api/positions');
  return response.data;
};
