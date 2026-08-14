import { useState } from 'react';
import { AlertTriangle, X } from 'lucide-react';
import { deleteEmployee } from '../services/employeeService';

export default function DeleteConfirmModal({ isOpen, onClose, onSuccess, employee }) {
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState(null);

  if (!isOpen || !employee) return null;

  const fullName = [employee.first_name, employee.last_name].filter(Boolean).join(' ');

  const handleDelete = async () => {
    setDeleting(true);
    setError(null);
    try {
      await deleteEmployee(employee.id);
      onSuccess();
      onClose();
    } catch (err) {
      const msg = err.response?.data?.detail || err.response?.data?.message || 'Failed to delete employee';
      setError(typeof msg === 'string' ? msg : 'Failed to delete employee');
    } finally {
      setDeleting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/40 backdrop-blur-sm" onClick={onClose} />
      <div className="relative bg-white rounded-2xl shadow-2xl w-full max-w-md mx-4 p-6">
        <button onClick={onClose} className="absolute top-4 right-4 w-8 h-8 rounded-lg flex items-center justify-center hover:bg-surface-100 transition-colors" aria-label="Close">
          <X className="w-5 h-5 text-surface-500" />
        </button>

        <div className="flex flex-col items-center text-center">
          <div className="w-14 h-14 rounded-full bg-red-100 flex items-center justify-center mb-4">
            <AlertTriangle className="w-7 h-7 text-red-600" />
          </div>

          <h2 className="text-lg font-bold text-surface-900 mb-2">Delete Employee</h2>
          <p className="text-sm text-surface-600 mb-1">
            Are you sure you want to delete <span className="font-semibold">{fullName}</span>?
          </p>
          <p className="text-xs text-surface-400 mb-5">
            Employee ID: {employee.employee_id}. This action cannot be undone.
          </p>

          {error && (
            <div className="w-full mb-4 p-3 rounded-lg bg-red-50 border border-red-200 text-sm text-red-700">{error}</div>
          )}

          <div className="flex items-center gap-3 w-full">
            <button type="button" onClick={onClose} className="flex-1 px-4 py-2.5 rounded-lg text-sm font-medium text-surface-600 border border-surface-300 hover:bg-surface-50 transition-colors">
              Cancel
            </button>
            <button type="button" onClick={handleDelete} disabled={deleting} className="flex-1 px-4 py-2.5 rounded-lg text-sm font-semibold text-white bg-red-600 hover:bg-red-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed">
              {deleting ? 'Deleting...' : 'Delete'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
