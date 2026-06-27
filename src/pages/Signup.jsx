import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Input from '../components/Input';
import Button from '../components/Button';
import API from '../api';

const parseError = (err) => {
  if (!err.response) return null; // network error — handled separately
  const detail = err.response?.data?.detail;
  if (!detail) return 'Sign up failed. Please try again.';
  if (typeof detail === 'string') return detail;
  if (Array.isArray(detail)) return detail.map(d => d.msg).join(', ');
  return 'Sign up failed. Please try again.';
};

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

const Signup = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [status, setStatus] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async e => {
    e.preventDefault();
    if (password.length < 8) {
      setError('Password must be at least 8 characters.');
      return;
    }
    setError('');
    setLoading(true);

    for (let attempt = 1; attempt <= 3; attempt++) {
      try {
        setStatus(attempt === 1 ? 'Signing up…' : `Backend waking up, retrying… (${attempt}/3)`);
        await API.post('/auth/signup', { email, password });
        navigate('/login');
        return;
      } catch (err) {
        const msg = parseError(err);
        if (msg) {
          // Real API error (wrong email, already registered, etc.) — don't retry
          setError(msg);
          setStatus('');
          setLoading(false);
          return;
        }
        // Network error — Render is sleeping, wait and retry
        if (attempt < 3) {
          setStatus(`Backend is starting up… retrying in 15s (${attempt}/3)`);
          await sleep(15000);
        }
      }
    }

    setError('Backend took too long to respond. Wait 30 seconds then try again.');
    setStatus('');
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex items-center justify-center p-4">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <div className="w-12 h-12 rounded-2xl bg-indigo-600 mx-auto mb-3 flex items-center justify-center">
            <span className="text-white font-bold text-xl">A</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Create account</h1>
          <p className="text-slate-500 dark:text-slate-400 text-sm mt-1">Join us today</p>
        </div>
        <form onSubmit={handleSubmit} className="bg-white dark:bg-slate-800 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-700 p-6 space-y-4">
          <Input label="Email" type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="you@example.com" required />
          <div className="space-y-1">
            <Input label="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Min. 8 characters" required />
            <p className="text-xs text-slate-400">Must be at least 8 characters</p>
          </div>
          {error && <p className="text-red-500 text-sm">{error}</p>}
          {status && <p className="text-indigo-500 text-sm">{status}</p>}
          <Button type="submit" className="w-full justify-center" disabled={loading}>
            {loading ? status || 'Signing up…' : 'Sign Up'}
          </Button>
        </form>
        <p className="text-center text-sm text-slate-500 mt-4">
          Already have an account? <Link to="/login" className="text-indigo-600 font-medium hover:underline">Sign in</Link>
        </p>
      </div>
    </div>
  );
};

export default Signup;
