import { Network } from 'lucide-react';
import OrgChart from '../components/OrgChart';

export default function Organization() {
  return (
    <div className="p-8">

      <div className="mb-6">
        <div className="flex items-center gap-3 mb-1">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-primary-500 to-primary-700 flex items-center justify-center shadow-lg shadow-primary-500/20">
            <Network className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-surface-900">Organization Chart</h1>
            <p className="text-sm text-surface-500">Visual representation of the reporting hierarchy</p>
          </div>
        </div>
      </div>


      <OrgChart />
    </div>
  );
}
