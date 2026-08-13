import { useNavigate } from 'react-router-dom';
import EmployeeAvatar from './EmployeeAvatar';
import { formatFullName } from '../utils/formatName';

export default function EmployeeInfoCard({ employee }) {
  const navigate = useNavigate();

  if (!employee) return null;

  return (
    <button
      onClick={() => navigate(`/employee/${employee.id}`)}
      className="flex items-center gap-3 p-3 rounded-lg hover:bg-surface-50 transition-colors w-full text-left group"
      aria-label={`View profile of ${formatFullName(employee.first_name, employee.last_name)}`}
    >
      <EmployeeAvatar
        firstName={employee.first_name}
        lastName={employee.last_name}
        profileImage={employee.profile_image}
        size="sm"
      />
      <div className="min-w-0">
        <p className="text-sm font-medium text-primary-600 group-hover:text-primary-700 truncate">
          {formatFullName(employee.first_name, employee.last_name)}
        </p>
        {employee.position_title && (
          <p className="text-xs text-surface-500 truncate">{employee.position_title}</p>
        )}
        <p className="text-xs text-surface-400 font-mono">{employee.employee_id}</p>
      </div>
    </button>
  );
}
