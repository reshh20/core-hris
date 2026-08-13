import { Users } from 'lucide-react';
import { useEmployees } from '../hooks/useEmployees';
import SearchBar from '../components/SearchBar';
import FilterControls from '../components/FilterControls';
import EmployeeTable from '../components/EmployeeTable';
import LoadingState from '../components/LoadingState';
import EmptyState from '../components/EmptyState';
import ErrorState from '../components/ErrorState';

export default function Employees() {
  const {
    employees,
    departments,
    loading,
    error,
    filters,
    updateFilter,
    clearFilters,
    refresh,
  } = useEmployees();

  return (
    <div className="p-8">
      {/* Page Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-1">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-primary-500 to-primary-700 flex items-center justify-center shadow-lg shadow-primary-500/20">
            <Users className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-surface-900">Employee Directory</h1>
            <p className="text-sm text-surface-500">
              {!loading && `${employees.length} employee${employees.length !== 1 ? 's' : ''} found`}
            </p>
          </div>
        </div>
      </div>

      {/* Search & Filters */}
      <div className="flex flex-col sm:flex-row gap-4 mb-6">
        <div className="flex-1 max-w-md">
          <SearchBar
            value={filters.search}
            onChange={(value) => updateFilter('search', value)}
            placeholder="Search by name, ID, or email..."
          />
        </div>
        <FilterControls
          departments={departments}
          filters={filters}
          onFilterChange={updateFilter}
          onClear={clearFilters}
        />
      </div>

      {/* Content */}
      {loading ? (
        <LoadingState message="Loading employees..." />
      ) : error ? (
        <ErrorState message={error} onRetry={refresh} />
      ) : employees.length === 0 ? (
        <EmptyState
          title="No Employees Found"
          message={
            filters.search || filters.department_id || filters.status
              ? 'No employees match your current filters. Try adjusting your search criteria.'
              : 'No employees in the system yet.'
          }
        />
      ) : (
        <EmployeeTable employees={employees} />
      )}
    </div>
  );
}
