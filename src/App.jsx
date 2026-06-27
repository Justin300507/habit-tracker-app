import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Signup from './pages/Signup';
import PasswordResetRequest from './pages/PasswordResetRequest';
import PasswordReset from './pages/PasswordReset';
import Dashboard from './pages/Dashboard';
import HabitList from './pages/HabitList';
import HabitDetail from './pages/HabitDetail';
import HabitEdit from './pages/HabitEdit';
import Sidebar from './components/Sidebar';
import Header from './components/Header';

const Layout = ({ children }) => (
  <div className="flex min-h-screen bg-slate-50 dark:bg-slate-900">
    <Sidebar />
    <main className="ml-56 flex-1 p-6 overflow-auto">
      <Header />
      {children}
    </main>
  </div>
);

const App = () => (
  <Router>
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Signup />} />
      <Route path="/password-reset-request" element={<PasswordResetRequest />} />
      <Route path="/password-reset" element={<PasswordReset />} />
      <Route path="/dashboard" element={<Layout><Dashboard /></Layout>} />
      <Route path="/habits" element={<Layout><HabitList /></Layout>} />
      <Route path="/habits/:habitId" element={<Layout><HabitDetail /></Layout>} />
      <Route path="/habits/:habitId/edit" element={<Layout><HabitEdit /></Layout>} />
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  </Router>
);

export default App;