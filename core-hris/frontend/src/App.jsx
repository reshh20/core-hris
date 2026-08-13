import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Employees from './pages/Employees';
import EmployeeProfile from './pages/EmployeeProfile';
import Organization from './pages/Organization';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/employees" element={<Employees />} />
          <Route path="/employee/:id" element={<EmployeeProfile />} />
          <Route path="/organization" element={<Organization />} />
          <Route path="/" element={<Navigate to="/employees" replace />} />
          <Route path="*" element={<Navigate to="/employees" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
