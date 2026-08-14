import api from './api';


export const fetchEmployees = async (params = {}) => {
  const response = await api.get('/api/employees', { params });
  return response.data;
};


export const fetchEmployee = async (id) => {
  const response = await api.get(`/api/employees/${id}`);
  return response.data;
};


export const fetchDepartments = async () => {
  const response = await api.get('/api/departments');
  return response.data;
};


export const fetchPositions = async () => {
  const response = await api.get('/api/positions');
  return response.data;
};

export const createEmployee = async (employeeData) => {
  const response = await api.post('/api/employees', employeeData);
  return response.data;
};

export const updateEmployee = async (id, employeeData) => {
  const response = await api.put(`/api/employees/${id}`, employeeData);
  return response.data;
};

export const deleteEmployee = async (id) => {
  const response = await api.delete(`/api/employees/${id}`);
  return response.data;
};
