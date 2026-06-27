import React, { useState } from 'react';
import Input from '../components/Input';
import Button from '../components/Button';
import API from '../api';
import { useSearchParams } from 'react-router-dom';

const PasswordReset = () => {
  const [password, setPassword] = useState('');
  const [token, setToken] = useState('');
  const [searchParams] = useSearchParams();
  const handleSubmit = async e => {
    e.preventDefault();
    try {
      await API.post('/auth/password-reset', { token, new_password: password });
    } catch (err) {}
  };
  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex items-center justify-center p-4">
      <div className="w-full max-w-sm">
        <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-4">Set New Password</h2>
        <form onSubmit={handleSubmit} className="bg-white dark:bg-slate-800 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-700 p-6 space-y-4">
          <Input label="Reset Token" value={token} onChange={e => setToken(e.target.value)} placeholder="Token from email" />
          <Input label="New Password" type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="********" />
          <Button type="submit" className="w-full justify-center">Reset Password</Button>
        </form>
      </div>
    </div>
  );
};

export default PasswordReset;