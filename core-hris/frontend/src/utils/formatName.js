
export function formatFullName(firstName, lastName) {
  return [firstName, lastName].filter(Boolean).join(' ') || 'Unknown';
}


export function getInitials(firstName, lastName) {
  const first = (firstName || '').charAt(0).toUpperCase();
  const last = (lastName || '').charAt(0).toUpperCase();
  return `${first}${last}` || '?';
}
