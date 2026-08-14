import { useState, useEffect, useCallback } from 'react';
import { fetchEmployees, fetchDepartments } from '../services/employeeService';


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
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(1);

  const loadEmployees = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const params = {};
      if (filters.search) params.search = filters.search;
      if (filters.department_id) params.department_id = filters.department_id;
      if (filters.status) params.status = filters.status;
      params.page = page;
      params.per_page = 10;

      const data = await fetchEmployees(params);
      setEmployees(data.items || []);
      setTotal(data.total || 0);
      setTotalPages(data.total_pages || 1);
    } catch (err) {
      setError(err.friendlyMessage || 'Failed to load employees');
    } finally {
      setLoading(false);
    }
  }, [filters, page]);

  const loadDepartments = useCallback(async () => {
    try {
      const data = await fetchDepartments();
      setDepartments(data);
    } catch {

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
    setPage(1);
  };

  const clearFilters = () => {
    setFilters({ search: '', department_id: '', status: '' });
    setPage(1);
  };

  return {
    employees,
    departments,
    loading,
    error,
    filters,
    page,
    total,
    totalPages,
    setPage,
    updateFilter,
    clearFilters,
    refresh: loadEmployees,
  };
}
