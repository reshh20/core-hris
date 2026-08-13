import { NavLink, Outlet } from 'react-router-dom';
import { Users, Network, Heart } from 'lucide-react';

const navItems = [
  { to: '/employees', label: 'Employees', icon: Users },
  { to: '/organization', label: 'Organization', icon: Network },
];

export default function Layout() {
  return (
    <div className="flex h-screen overflow-hidden bg-surface-100">
      {/* Sidebar */}
      <aside className="w-64 flex-shrink-0 bg-surface-900 text-white flex flex-col shadow-xl">
        {/* Brand */}
        <div className="p-6 border-b border-surface-700/50">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-primary-400 to-primary-600 flex items-center justify-center">
              <Heart className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-lg font-bold tracking-tight">Core HRIS</h1>
              <p className="text-xs text-surface-400 font-medium">Employee Management</p>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-3 py-4 space-y-1" aria-label="Main navigation">
          {navItems.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 ${
                  isActive
                    ? 'bg-primary-600 text-white shadow-lg shadow-primary-600/25'
                    : 'text-surface-300 hover:bg-surface-800 hover:text-white'
                }`
              }
              aria-label={label}
            >
              <Icon className="w-5 h-5 flex-shrink-0" />
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>

        {/* Footer */}
        <div className="p-4 border-t border-surface-700/50">
          <p className="text-xs text-surface-500 text-center">© 2024 Core HRIS v1.0</p>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto">
        <Outlet />
      </main>
    </div>
  );
}
