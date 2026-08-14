import { X } from 'lucide-react';

const STATUSES = [
  { value: '', label: 'All Statuses' },
  { value: 'ACTIVE', label: 'Active' },
  { value: 'ON_LEAVE', label: 'On Leave' },
  { value: 'RESIGNED', label: 'Resigned' },
  { value: 'TERMINATED', label: 'Terminated' },
];

export default function FilterControls({
  departments,
  filters,
  onFilterChange,
  onClear,
}) {
  const hasActiveFilters = filters.department_id || filters.status;

  return (
    <div className="flex flex-wrap items-center gap-3">

      <select
        value={filters.department_id}
        onChange={(e) => onFilterChange('department_id', e.target.value)}
        className="px-3 py-2.5 bg-white border border-surface-200 rounded-lg text-sm text-surface-700 focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-400 transition-all cursor-pointer"
        aria-label="Filter by department"
        id="department-filter"
      >
        <option value="">All Departments</option>
        {departments.map((dept) => (
          <option key={dept.id} value={dept.id}>
            {dept.name}
          </option>
        ))}
      </select>


      <select
        value={filters.status}
        onChange={(e) => onFilterChange('status', e.target.value)}
        className="px-3 py-2.5 bg-white border border-surface-200 rounded-lg text-sm text-surface-700 focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-400 transition-all cursor-pointer"
        aria-label="Filter by status"
        id="status-filter"
      >
        {STATUSES.map((s) => (
          <option key={s.value} value={s.value}>
            {s.label}
          </option>
        ))}
      </select>


      {hasActiveFilters && (
        <button
          onClick={onClear}
          className="flex items-center gap-1.5 px-3 py-2.5 text-sm text-surface-500 hover:text-surface-700 hover:bg-surface-100 rounded-lg transition-all"
          aria-label="Clear all filters"
          id="clear-filters-btn"
        >
          <X className="w-4 h-4" />
          Clear Filters
        </button>
      )}
    </div>
  );
}
