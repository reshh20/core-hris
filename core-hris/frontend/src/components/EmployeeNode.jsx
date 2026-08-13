import { useNavigate } from 'react-router-dom';
import { getInitials } from '../utils/formatName';

/**
 * Custom React Flow node for the organization chart.
 */
export default function EmployeeNode({ data }) {
  const navigate = useNavigate();
  const { firstName, lastName, positionTitle, departmentName, profileImage, employeeId } = data;
  const initials = getInitials(firstName, lastName);
  const fullName = [firstName, lastName].filter(Boolean).join(' ');

  const handleClick = (e) => {
    e.stopPropagation();
    if (employeeId) {
      navigate(`/employee/${employeeId}`);
    }
  };

  return (
    <div
      onClick={handleClick}
      className="bg-white rounded-xl border-2 border-surface-200 shadow-md hover:shadow-lg hover:border-primary-300 transition-all duration-200 cursor-pointer px-5 py-4 min-w-[200px]"
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          handleClick(e);
        }
      }}
      aria-label={`${fullName}, ${positionTitle}`}
    >
      <div className="flex items-center gap-3">
        {profileImage ? (
          <img
            src={profileImage}
            alt={fullName}
            className="w-10 h-10 rounded-full object-cover ring-2 ring-primary-100"
          />
        ) : (
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary-400 to-primary-600 flex items-center justify-center text-white text-sm font-semibold ring-2 ring-primary-100">
            {initials}
          </div>
        )}
        <div className="min-w-0">
          <p className="text-sm font-semibold text-surface-800 truncate">{fullName}</p>
          <p className="text-xs text-primary-600 font-medium truncate">{positionTitle || 'N/A'}</p>
          <p className="text-[11px] text-surface-400 truncate">{departmentName || ''}</p>
        </div>
      </div>
    </div>
  );
}
