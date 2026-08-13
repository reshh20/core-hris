import { getInitials } from '../utils/formatName';

const AVATAR_COLORS = [
  'from-primary-400 to-primary-600',
  'from-emerald-400 to-emerald-600',
  'from-amber-400 to-amber-600',
  'from-rose-400 to-rose-600',
  'from-cyan-400 to-cyan-600',
  'from-violet-400 to-violet-600',
  'from-fuchsia-400 to-fuchsia-600',
  'from-teal-400 to-teal-600',
];

/**
 * Deterministic color based on name.
 */
function getColorClass(firstName, lastName) {
  const str = `${firstName}${lastName}`;
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash);
  }
  return AVATAR_COLORS[Math.abs(hash) % AVATAR_COLORS.length];
}

const sizeClasses = {
  sm: 'w-8 h-8 text-xs',
  md: 'w-10 h-10 text-sm',
  lg: 'w-14 h-14 text-lg',
  xl: 'w-20 h-20 text-2xl',
};

export default function EmployeeAvatar({
  firstName,
  lastName,
  profileImage,
  size = 'md',
  className = '',
}) {
  const initials = getInitials(firstName, lastName);
  const sizeClass = sizeClasses[size] || sizeClasses.md;
  const colorClass = getColorClass(firstName, lastName);

  if (profileImage) {
    return (
      <img
        src={profileImage}
        alt={`${firstName} ${lastName}`}
        className={`${sizeClass} rounded-full object-cover ring-2 ring-white shadow-sm ${className}`}
      />
    );
  }

  return (
    <div
      className={`${sizeClass} rounded-full bg-gradient-to-br ${colorClass} flex items-center justify-center text-white font-semibold ring-2 ring-white shadow-sm ${className}`}
      role="img"
      aria-label={`Avatar for ${firstName} ${lastName}`}
    >
      {initials}
    </div>
  );
}
