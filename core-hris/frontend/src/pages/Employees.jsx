import { useState } from 'react';
import { Users, Plus } from 'lucide-react';
import { useEmployees } from '../hooks/useEmployees';
import SearchBar from '../components/SearchBar';
import FilterControls from '../components/FilterControls';
import EmployeeTable from '../components/EmployeeTable';
import LoadingState from '../components/LoadingState';
import EmptyState from '../components/EmptyState';
import ErrorState from '../components/ErrorState';
import AddEmployeeModal from '../components/AddEmployeeModal';

export default function Employees() {
  const {
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
    refresh,
  } = useEmployees();

  const [showAddModal, setShowAddModal] = useState(false);

  return (
    <div className="p-8">

      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3 mb-1">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-primary-500 to-primary-700 flex items-center justify-center shadow-lg shadow-primary-500/20">
              <Users className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-surface-900">Employee Directory</h1>
              <p className="text-sm text-surface-500">
                {!loading && `${total} employee${total !== 1 ? 's' : ''} found`}
              </p>
            </div>
          </div>
          <button
            onClick={() => setShowAddModal(true)}
            className="flex items-center gap-2 px-4 py-2.5 rounded-lg text-sm font-semibold text-white bg-gradient-to-r from-primary-500 to-primary-700 hover:from-primary-600 hover:to-primary-800 shadow-lg shadow-primary-500/25 transition-all"
            id="add-employee-btn"
          >
            <Plus className="w-4 h-4" />
            Add Employee
          </button>
        </div>
      </div>

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
        <>
          <EmployeeTable employees={employees} />
          {total > 0 && (
            <div className="flex items-center justify-between px-4 py-3 bg-white border border-surface-200 sm:px-6 mt-4 rounded-xl shadow-sm">
              <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
                <div>
                  <p className="text-sm text-surface-700">
                    Showing <span className="font-medium">{(page - 1) * 10 + 1}</span> to <span className="font-medium">{Math.min(page * 10, total)}</span> of{' '}
                    <span className="font-medium">{total}</span> results
                  </p>
                </div>
                <div>
                  <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                    <button
                      onClick={() => setPage(page - 1)}
                      disabled={page === 1}
                      className="relative inline-flex items-center px-4 py-2 border border-surface-300 text-sm font-medium rounded-l-md text-surface-700 bg-white hover:bg-surface-50 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      Previous
                    </button>
                    <button
                      onClick={() => setPage(page + 1)}
                      disabled={page === totalPages || totalPages === 0}
                      className="relative inline-flex items-center px-4 py-2 border border-surface-300 text-sm font-medium rounded-r-md text-surface-700 bg-white hover:bg-surface-50 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      Next
                    </button>
                  </nav>
                </div>
              </div>
            </div>
          )}
        </>
      )}

      <AddEmployeeModal
        isOpen={showAddModal}
        onClose={() => setShowAddModal(false)}
        onSuccess={refresh}
      />
    </div>
  );
}
