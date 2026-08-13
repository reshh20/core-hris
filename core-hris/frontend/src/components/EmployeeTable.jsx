import { useNavigate } from 'react-router-dom';
import EmployeeAvatar from './EmployeeAvatar';
import StatusBadge from './StatusBadge';
import { formatFullName } from '../utils/formatName';

export default function EmployeeTable({ employees }) {
  const navigate = useNavigate();

  return (
    <div className="bg-white rounded-xl border border-surface-200 shadow-sm overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full" role="table" aria-label="Employee directory">
          <thead>
            <tr className="border-b border-surface-200 bg-surface-50/50">
              <th className="text-left px-6 py-3.5 text-xs font-semibold text-surface-500 uppercase tracking-wider">Employee</th>
              <th className="text-left px-6 py-3.5 text-xs font-semibold text-surface-500 uppercase tracking-wider">Employee ID</th>
              <th className="text-left px-6 py-3.5 text-xs font-semibold text-surface-500 uppercase tracking-wider">Department</th>
              <th className="text-left px-6 py-3.5 text-xs font-semibold text-surface-500 uppercase tracking-wider">Position</th>
              <th className="text-left px-6 py-3.5 text-xs font-semibold text-surface-500 uppercase tracking-wider">Location</th>
              <th className="text-left px-6 py-3.5 text-xs font-semibold text-surface-500 uppercase tracking-wider">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-surface-100">
            {employees.map((employee) => (
              <tr
                key={employee.id}
                onClick={() => navigate(`/employee/${employee.id}`)}
                className="hover:bg-primary-50/30 cursor-pointer transition-colors duration-150"
                role="row"
                tabIndex={0}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    navigate(`/employee/${employee.id}`);
                  }
                }}
                aria-label={`View details for ${formatFullName(employee.first_name, employee.last_name)}`}
              >
                <td className="px-6 py-4">
                  <div className="flex items-center gap-3">
                    <EmployeeAvatar
                      firstName={employee.first_name}
                      lastName={employee.last_name}
                      profileImage={employee.profile_image}
                      size="sm"
                    />
                    <span className="font-medium text-sm text-surface-800">
                      {formatFullName(employee.first_name, employee.last_name)}
                    </span>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <span className="text-sm text-surface-500 font-mono">{employee.employee_id}</span>
                </td>
                <td className="px-6 py-4">
                  <span className="text-sm text-surface-600">{employee.department?.name || 'N/A'}</span>
                </td>
                <td className="px-6 py-4">
                  <span className="text-sm text-surface-600">{employee.position?.title || 'N/A'}</span>
                </td>
                <td className="px-6 py-4">
                  <span className="text-sm text-surface-500">{employee.location}</span>
                </td>
                <td className="px-6 py-4">
                  <StatusBadge status={employee.employment_status} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
