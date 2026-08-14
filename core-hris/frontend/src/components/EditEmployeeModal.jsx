import { useState, useEffect } from 'react';
import { X } from 'lucide-react';
import { updateEmployee, fetchDepartments, fetchPositions, fetchEmployees } from '../services/employeeService';

export default function EditEmployeeModal({ isOpen, onClose, onSuccess, employee }) {
  const [form, setForm] = useState({});
  const [departments, setDepartments] = useState([]);
  const [positions, setPositions] = useState([]);
  const [allEmployees, setAllEmployees] = useState([]);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [fieldErrors, setFieldErrors] = useState({});

  useEffect(() => {
    if (isOpen && employee) {
      setForm({
        employee_id: employee.employee_id || '',
        first_name: employee.first_name || '',
        last_name: employee.last_name || '',
        email: employee.email || '',
        phone: employee.phone || '',
        department_id: employee.department_id?.toString() || '',
        position_id: employee.position_id?.toString() || '',
        manager_id: employee.manager_id?.toString() || '',
        location: employee.location || '',
        joining_date: employee.joining_date || '',
        employment_status: employee.employment_status || 'ACTIVE',
        profile_image: employee.profile_image || '',
      });
      setError(null);
      setFieldErrors({});
      Promise.all([fetchDepartments(), fetchPositions(), fetchEmployees()])
        .then(([depts, pos, emps]) => {
          setDepartments(depts);
          setPositions(pos);
          setAllEmployees(emps.filter((e) => e.id !== employee.id));
        })
        .catch(() => { });
    }
  }, [isOpen, employee]);

  if (!isOpen || !employee) return null;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    setFieldErrors((prev) => ({ ...prev, [name]: null }));
  };

  const validate = () => {
    const errors = {};
    if (!form.employee_id) errors.employee_id = 'Required';
    else if (!/^EMP\d{3,}$/.test(form.employee_id)) errors.employee_id = 'Format: EMP followed by 3+ digits';
    if (!form.first_name.trim()) errors.first_name = 'Required';
    if (!form.last_name.trim()) errors.last_name = 'Required';
    if (!form.email.trim()) errors.email = 'Required';
    if (!form.phone.trim()) errors.phone = 'Required';
    if (!form.department_id) errors.department_id = 'Required';
    if (!form.position_id) errors.position_id = 'Required';
    if (!form.location.trim()) errors.location = 'Required';
    if (!form.joining_date) errors.joining_date = 'Required';
    if (!form.employment_status) errors.employment_status = 'Required';
    return errors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const errors = validate();
    if (Object.keys(errors).length > 0) {
      setFieldErrors(errors);
      return;
    }

    setSubmitting(true);
    setError(null);

    try {
      const payload = {
        ...form,
        department_id: parseInt(form.department_id, 10),
        position_id: parseInt(form.position_id, 10),
        manager_id: form.manager_id ? parseInt(form.manager_id, 10) : null,
        profile_image: form.profile_image.trim() || null,
      };
      await updateEmployee(employee.id, payload);
      onSuccess();
      onClose();
    } catch (err) {
      const msg = err.response?.data?.detail || err.response?.data?.message || 'Failed to update employee';
      if (typeof msg === 'string') {
        setError(msg);
      } else if (Array.isArray(msg)) {
        const parsed = {};
        msg.forEach((e) => {
          const field = e.loc?.[e.loc.length - 1];
          if (field) parsed[field] = e.msg;
        });
        if (Object.keys(parsed).length > 0) setFieldErrors(parsed);
        else setError('Validation error. Please check your inputs.');
      } else {
        setError('Failed to update employee');
      }
    } finally {
      setSubmitting(false);
    }
  };

  const inputClass = (field) =>
    `w-full px-3 py-2.5 rounded-lg border text-sm transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500/30 ${fieldErrors[field]
      ? 'border-red-400 bg-red-50/50 focus:border-red-500'
      : 'border-surface-300 bg-white focus:border-primary-400'
    }`;

  const labelClass = 'block text-xs font-semibold text-surface-600 mb-1.5 uppercase tracking-wider';

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/40 backdrop-blur-sm" onClick={onClose} />
      <div className="relative bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto mx-4">
        <div className="sticky top-0 bg-white border-b border-surface-200 px-6 py-4 rounded-t-2xl flex items-center justify-between z-10">
          <h2 className="text-lg font-bold text-surface-900">Edit Employee</h2>
          <button onClick={onClose} className="w-8 h-8 rounded-lg flex items-center justify-center hover:bg-surface-100 transition-colors" aria-label="Close">
            <X className="w-5 h-5 text-surface-500" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6">
          {error && (
            <div className="mb-5 p-3 rounded-lg bg-red-50 border border-red-200 text-sm text-red-700">{error}</div>
          )}

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-5 gap-y-4">
            <div>
              <label className={labelClass}>Employee ID *</label>
              <input name="employee_id" value={form.employee_id} onChange={handleChange} className={inputClass('employee_id')} />
              {fieldErrors.employee_id && <p className="text-xs text-red-500 mt-1">{fieldErrors.employee_id}</p>}
            </div>

            <div>
              <label className={labelClass}>Email *</label>
              <input name="email" type="email" value={form.email} onChange={handleChange} className={inputClass('email')} />
              {fieldErrors.email && <p className="text-xs text-red-500 mt-1">{fieldErrors.email}</p>}
            </div>

            <div>
              <label className={labelClass}>First Name *</label>
              <input name="first_name" value={form.first_name} onChange={handleChange} className={inputClass('first_name')} />
              {fieldErrors.first_name && <p className="text-xs text-red-500 mt-1">{fieldErrors.first_name}</p>}
            </div>

            <div>
              <label className={labelClass}>Last Name *</label>
              <input name="last_name" value={form.last_name} onChange={handleChange} className={inputClass('last_name')} />
              {fieldErrors.last_name && <p className="text-xs text-red-500 mt-1">{fieldErrors.last_name}</p>}
            </div>

            <div>
              <label className={labelClass}>Phone *</label>
              <input name="phone" value={form.phone} onChange={handleChange} className={inputClass('phone')} />
              {fieldErrors.phone && <p className="text-xs text-red-500 mt-1">{fieldErrors.phone}</p>}
            </div>

            <div>
              <label className={labelClass}>Location *</label>
              <input name="location" value={form.location} onChange={handleChange} className={inputClass('location')} />
              {fieldErrors.location && <p className="text-xs text-red-500 mt-1">{fieldErrors.location}</p>}
            </div>

            <div>
              <label className={labelClass}>Department *</label>
              <select name="department_id" value={form.department_id} onChange={handleChange} className={inputClass('department_id')}>
                <option value="">Select Department</option>
                {departments.map((d) => (
                  <option key={d.id} value={d.id}>{d.name}</option>
                ))}
              </select>
              {fieldErrors.department_id && <p className="text-xs text-red-500 mt-1">{fieldErrors.department_id}</p>}
            </div>

            <div>
              <label className={labelClass}>Position *</label>
              <select name="position_id" value={form.position_id} onChange={handleChange} className={inputClass('position_id')}>
                <option value="">Select Position</option>
                {positions.map((p) => (
                  <option key={p.id} value={p.id}>{p.title}</option>
                ))}
              </select>
              {fieldErrors.position_id && <p className="text-xs text-red-500 mt-1">{fieldErrors.position_id}</p>}
            </div>

            <div>
              <label className={labelClass}>Manager (Reports To)</label>
              <select name="manager_id" value={form.manager_id} onChange={handleChange} className={inputClass('manager_id')}>
                <option value="">None (Top-level)</option>
                {allEmployees.map((emp) => (
                  <option key={emp.id} value={emp.id}>
                    {emp.first_name} {emp.last_name} ({emp.employee_id})
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className={labelClass}>Joining Date *</label>
              <input name="joining_date" type="date" value={form.joining_date} onChange={handleChange} max={new Date().toISOString().split('T')[0]} className={inputClass('joining_date')} />
              {fieldErrors.joining_date && <p className="text-xs text-red-500 mt-1">{fieldErrors.joining_date}</p>}
            </div>

            <div>
              <label className={labelClass}>Employment Status *</label>
              <select name="employment_status" value={form.employment_status} onChange={handleChange} className={inputClass('employment_status')}>
                <option value="ACTIVE">Active</option>
                <option value="ON_LEAVE">On Leave</option>
                <option value="RESIGNED">Resigned</option>
                <option value="TERMINATED">Terminated</option>
              </select>
            </div>

            <div>
              <label className={labelClass}>Profile Image URL</label>
              <input name="profile_image" value={form.profile_image} onChange={handleChange} placeholder="https://example.com/photo.jpg" className={inputClass('profile_image')} />
            </div>
          </div>

          <div className="flex items-center justify-end gap-3 mt-8 pt-5 border-t border-surface-200">
            <button type="button" onClick={onClose} className="px-5 py-2.5 rounded-lg text-sm font-medium text-surface-600 hover:bg-surface-100 transition-colors">
              Cancel
            </button>
            <button type="submit" disabled={submitting} className="px-5 py-2.5 rounded-lg text-sm font-semibold text-white bg-gradient-to-r from-primary-500 to-primary-700 hover:from-primary-600 hover:to-primary-800 shadow-lg shadow-primary-500/25 transition-all disabled:opacity-50 disabled:cursor-not-allowed">
              {submitting ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
