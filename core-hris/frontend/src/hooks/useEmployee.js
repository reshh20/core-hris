import { useState, useEffect, useCallback } from 'react';
import { fetchEmployee } from '../services/employeeService';

/**
 * Custom hook for fetching a single employee's details.
 */
export function useEmployee(id) {
  const [employee, setEmployee] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadEmployee = useCallback(async () => {
    if (!id) return;
    try {
      setLoading(true);
      setError(null);
      const data = await fetchEmployee(id);
      setEmployee(data);
    } catch (err) {
      if (err.response?.status === 404) {
        setError('Employee not found');
      } else {
        setError(err.friendlyMessage || 'Failed to load employee details');
      }
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    loadEmployee();
  }, [loadEmployee]);

  return { employee, loading, error, refresh: loadEmployee };
}
