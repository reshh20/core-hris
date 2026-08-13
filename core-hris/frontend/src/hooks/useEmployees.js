import { useState, useEffect, useCallback } from 'react';
import { fetchEmployees, fetchDepartments } from '../services/employeeService';

/**
 * Custom hook for managing employee list state with search/filter.
 */
export function useEmployees() {
  const [employees, setEmployees] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    search: '',
    department_id: '',
    status: '',
  });

  const loadEmployees = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const params = {};
      if (filters.search) params.search = filters.search;
      if (filters.department_id) params.department_id = filters.department_id;
      if (filters.status) params.status = filters.status;

      const data = await fetchEmployees(params);
      setEmployees(data);
    } catch (err) {
      setError(err.friendlyMessage || 'Failed to load employees');
    } finally {
      setLoading(false);
    }
  }, [filters]);

  const loadDepartments = useCallback(async () => {
    try {
      const data = await fetchDepartments();
      setDepartments(data);
    } catch {
      // Silently fail — departments are secondary
    }
  }, []);

  useEffect(() => {
    loadDepartments();
  }, [loadDepartments]);

  useEffect(() => {
    const debounce = setTimeout(() => {
      loadEmployees();
    }, 300);
    return () => clearTimeout(debounce);
  }, [loadEmployees]);

  const updateFilter = (key, value) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  const clearFilters = () => {
    setFilters({ search: '', department_id: '', status: '' });
  };

  return {
    employees,
    departments,
    loading,
    error,
    filters,
    updateFilter,
    clearFilters,
    refresh: loadEmployees,
  };
}
