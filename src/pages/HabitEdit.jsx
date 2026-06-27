import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import HabitForm from '../components/HabitForm';
import LoadingSpinner from '../components/LoadingSpinner';
import API from '../api';

const parseError = (err) => {
  const detail = err.response?.data?.detail;
  if (!detail) return err.message || 'Failed to save habit.';
  if (typeof detail === 'string') return detail;
  if (Array.isArray(detail)) return detail.map(d => d.msg).join(', ');
  return 'Failed to save habit.';
};

const HabitEdit = () => {
  const { habitId } = useParams();
  const navigate = useNavigate();
  const [habit, setHabit] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchHabit = async () => {
      try {
        const res = await API.get(`/habits/${habitId}`);
        setHabit(res.data);
      } catch (err) {
        if (err.response?.status === 404) navigate('/habits');
      }
      setLoading(false);
    };
    fetchHabit();
  }, [habitId]);

  const handleSubmit = async data => {
    setError('');
    setSaving(true);
    try {
      await API.put(`/habits/${habitId}`, { name: data.name, description: data.description || null, is_active: data.is_active });
      navigate(`/habits/${habitId}`);
    } catch (err) {
      setError(parseError(err));
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl p-6 border border-slate-100 dark:border-slate-700">
      <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-4">Edit Habit</h2>
      {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
      <HabitForm initialData={habit} onSubmit={handleSubmit} onCancel={() => navigate(-1)} saving={saving} />
    </div>
  );
};

export default HabitEdit;
