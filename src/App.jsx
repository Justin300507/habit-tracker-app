import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

const PrivateRoute = ({ children }) => {
  return localStorage.getItem('token') ? children : <Navigate to="/login" replace />;
};
import Login from './pages/Login';
import Signup from './pages/Signup';
import PasswordResetRequest from './pages/PasswordResetRequest';
import PasswordReset from './pages/PasswordReset';
import Dashboard from './pages/Dashboard';
import HabitList from './pages/HabitList';
import HabitDetail from './pages/HabitDetail';
import HabitEdit from './pages/HabitEdit';
import HabitNew from './pages/HabitNew';
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
      <Route path="/dashboard" element={<PrivateRoute><Layout><Dashboard /></Layout></PrivateRoute>} />
      <Route path="/habits" element={<PrivateRoute><Layout><HabitList /></Layout></PrivateRoute>} />
      <Route path="/habits/new" element={<PrivateRoute><Layout><HabitNew /></Layout></PrivateRoute>} />
      <Route path="/habits/:habitId" element={<PrivateRoute><Layout><HabitDetail /></Layout></PrivateRoute>} />
      <Route path="/habits/:habitId/edit" element={<PrivateRoute><Layout><HabitEdit /></Layout></PrivateRoute>} />
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  </Router>
);

export default App;