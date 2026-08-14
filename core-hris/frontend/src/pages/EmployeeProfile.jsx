import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  ArrowLeft,
  Mail,
  Phone,
  MapPin,
  Calendar,
  Briefcase,
  Building2,
  UserCircle,
  Users,
  Hash,
  Pencil,
  Trash2,
} from 'lucide-react';
import { useEmployee } from '../hooks/useEmployee';
import EmployeeAvatar from '../components/EmployeeAvatar';
import StatusBadge from '../components/StatusBadge';
import EmployeeInfoCard from '../components/EmployeeInfoCard';
import LoadingState from '../components/LoadingState';
import ErrorState from '../components/ErrorState';
import EditEmployeeModal from '../components/EditEmployeeModal';
import DeleteConfirmModal from '../components/DeleteConfirmModal';
import { formatFullName } from '../utils/formatName';
import { formatDate } from '../utils/formatDate';

function InfoRow({ icon: Icon, label, value }) {
  return (
    <div className="flex items-start gap-3 py-3">
      <div className="w-9 h-9 rounded-lg bg-surface-100 flex items-center justify-center flex-shrink-0 mt-0.5">
        <Icon className="w-4 h-4 text-surface-500" />
      </div>
      <div className="min-w-0">
        <p className="text-xs font-medium text-surface-400 uppercase tracking-wider mb-0.5">{label}</p>
        <p className="text-sm text-surface-800 font-medium break-words">{value || 'N/A'}</p>
      </div>
    </div>
  );
}

export default function EmployeeProfile() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { employee, loading, error, refresh } = useEmployee(id);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);

  if (loading) return <LoadingState message="Loading employee details..." />;
  if (error) {
    return (
      <div className="p-8">
        <button
          onClick={() => navigate('/employees')}
          className="flex items-center gap-2 text-sm text-surface-500 hover:text-surface-700 mb-6 transition-colors"
          id="back-to-employees"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Employees
        </button>
        <ErrorState message={error} onRetry={refresh} />
      </div>
    );
  }

  if (!employee) return null;

  const fullName = formatFullName(employee.first_name, employee.last_name);

  const handleDeleteSuccess = () => {
    navigate('/employees');
  };

  return (
    <div className="p-8 max-w-5xl">

      <div className="flex items-center justify-between mb-6">
        <button
          onClick={() => navigate('/employees')}
          className="flex items-center gap-2 text-sm text-surface-500 hover:text-surface-700 transition-colors"
          id="back-to-employees"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Employees
        </button>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowEditModal(true)}
            className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium text-primary-600 border border-primary-300 hover:bg-primary-50 transition-colors"
            id="edit-employee-btn"
          >
            <Pencil className="w-4 h-4" />
            Edit
          </button>
          <button
            onClick={() => setShowDeleteModal(true)}
            className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium text-red-600 border border-red-300 hover:bg-red-50 transition-colors"
            id="delete-employee-btn"
          >
            <Trash2 className="w-4 h-4" />
            Delete
          </button>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-surface-200 shadow-sm p-6 mb-6">
        <div className="flex flex-col sm:flex-row items-start gap-5">
          <EmployeeAvatar
            firstName={employee.first_name}
            lastName={employee.last_name}
            profileImage={employee.profile_image}
            size="xl"
          />
          <div className="flex-1 min-w-0">
            <h1 className="text-2xl font-bold text-surface-900 mb-1">{fullName}</h1>
            <p className="text-base text-primary-600 font-medium mb-1">
              {employee.position?.title || 'N/A'}
            </p>
            <p className="text-sm text-surface-500 mb-3">
              {employee.department?.name || 'N/A'}
            </p>
            <StatusBadge status={employee.employment_status} />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">

        <div className="bg-white rounded-xl border border-surface-200 shadow-sm p-6">
          <h2 className="text-base font-semibold text-surface-800 mb-4 flex items-center gap-2">
            <UserCircle className="w-5 h-5 text-primary-500" />
            Personal Information
          </h2>
          <div className="divide-y divide-surface-100">
            <InfoRow icon={Hash} label="Employee ID" value={employee.employee_id} />
            <InfoRow icon={UserCircle} label="Full Name" value={fullName} />
            <InfoRow icon={Mail} label="Email" value={employee.email} />
            <InfoRow icon={Phone} label="Phone" value={employee.phone} />
            <InfoRow icon={MapPin} label="Location" value={employee.location} />
          </div>
        </div>

        <div className="bg-white rounded-xl border border-surface-200 shadow-sm p-6">
          <h2 className="text-base font-semibold text-surface-800 mb-4 flex items-center gap-2">
            <Briefcase className="w-5 h-5 text-primary-500" />
            Employment Information
          </h2>
          <div className="divide-y divide-surface-100">
            <InfoRow icon={Building2} label="Department" value={employee.department?.name} />
            <InfoRow icon={Briefcase} label="Position" value={employee.position?.title} />
            <InfoRow icon={Calendar} label="Joining Date" value={formatDate(employee.joining_date)} />
            <div className="flex items-start gap-3 py-3">
              <div className="w-9 h-9 rounded-lg bg-surface-100 flex items-center justify-center flex-shrink-0 mt-0.5">
                <UserCircle className="w-4 h-4 text-surface-500" />
              </div>
              <div>
                <p className="text-xs font-medium text-surface-400 uppercase tracking-wider mb-1">Employment Status</p>
                <StatusBadge status={employee.employment_status} />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

        <div className="bg-white rounded-xl border border-surface-200 shadow-sm p-6">
          <h2 className="text-base font-semibold text-surface-800 mb-4 flex items-center gap-2">
            <UserCircle className="w-5 h-5 text-primary-500" />
            Reports To
          </h2>
          {employee.manager ? (
            <EmployeeInfoCard employee={employee.manager} />
          ) : (
            <p className="text-sm text-surface-400 italic py-3">
              No manager — top-level employee
            </p>
          )}
        </div>

        <div className="bg-white rounded-xl border border-surface-200 shadow-sm p-6">
          <h2 className="text-base font-semibold text-surface-800 mb-4 flex items-center gap-2">
            <Users className="w-5 h-5 text-primary-500" />
            Direct Reports
            {employee.direct_reports.length > 0 && (
              <span className="text-xs bg-primary-100 text-primary-600 px-2 py-0.5 rounded-full font-medium">
                {employee.direct_reports.length}
              </span>
            )}
          </h2>
          {employee.direct_reports.length > 0 ? (
            <div className="space-y-1">
              {employee.direct_reports.map((report) => (
                <EmployeeInfoCard key={report.id} employee={report} />
              ))}
            </div>
          ) : (
            <p className="text-sm text-surface-400 italic py-3">No direct reports</p>
          )}
        </div>
      </div>

      <EditEmployeeModal
        isOpen={showEditModal}
        onClose={() => setShowEditModal(false)}
        onSuccess={refresh}
        employee={employee}
      />

      <DeleteConfirmModal
        isOpen={showDeleteModal}
        onClose={() => setShowDeleteModal(false)}
        onSuccess={handleDeleteSuccess}
        employee={employee}
      />
    </div>
  );
}
