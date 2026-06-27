import React, { useState } from 'react';
import Input from '../components/Input';
import Button from '../components/Button';
import API from '../api';

const PasswordResetRequest = () => {
  const [email, setEmail] = useState('');
  const handleSubmit = async e => {
    e.preventDefault();
    try {
      await API.post('/auth/password-reset-request', { email });
    } catch (err) {}
  };
  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex items-center justify-center p-4">
      <div className="w-full max-w-sm">
        <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-4">Reset Password</h2>
        <form onSubmit={handleSubmit} className="bg-white dark:bg-slate-800 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-700 p-6 space-y-4">
          <Input label="Email" value={email} onChange={e => setEmail(e.target.value)} placeholder="you@example.com" />
          <Button type="submit" className="w-full justify-center">Send Reset Link</Button>
        </form>
      </div>
    </div>
  );
};

export default PasswordResetRequest;