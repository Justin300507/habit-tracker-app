import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import HabitForm from '../components/HabitForm';
import API from '../api';

const parseError = (err) => {
  const detail = err.response?.data?.detail;
  if (!detail) return err.message || 'Failed to create habit.';
  if (typeof detail === 'string') return detail;
  if (Array.isArray(detail)) return detail.map(d => d.msg).join(', ');
  return 'Failed to create habit.';
};

const HabitNew = () => {
  const navigate = useNavigate();
  const [error, setError] = useState('');
  const [saving, setSaving] = useState(false);

  const handleSubmit = async data => {
    setError('');
    setSaving(true);
    try {
      const res = await API.post('/habits', { name: data.name, description: data.description || null });
      navigate(`/habits/${res.data.id}`);
    } catch (err) {
      setError(parseError(err));
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl p-6 border border-slate-100 dark:border-slate-700">
      <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-4">New Habit</h2>
      {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
      <HabitForm onSubmit={handleSubmit} onCancel={() => navigate('/habits')} saving={saving} />
    </div>
  );
};

export default HabitNew;
