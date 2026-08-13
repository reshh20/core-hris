import { Users } from 'lucide-react';

export default function EmptyState({ title = 'No data found', message = 'There are no records to display.' }) {
  return (
    <div className="flex flex-col items-center justify-center py-20 text-center">
      <div className="w-16 h-16 rounded-full bg-surface-100 flex items-center justify-center mb-4">
        <Users className="w-8 h-8 text-surface-400" />
      </div>
      <h3 className="text-lg font-semibold text-surface-700 mb-1">{title}</h3>
      <p className="text-sm text-surface-500 max-w-sm">{message}</p>
    </div>
  );
}
