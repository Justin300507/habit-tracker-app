import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import HabitForm from '../components/HabitForm';
import LoadingSpinner from '../components/LoadingSpinner';
import API from '../api';
import Button from '../components/Button';

const HabitEdit = () => {
  const { habitId } = useParams();
  const navigate = useNavigate();
  const [habit, setHabit] = useState(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    const fetchHabit = async () => {
      try {
        const res = await API.get(`/habits/${habitId}`);
        setHabit(res.data);
      } catch (err) {}
      setLoading(false);
    };
    fetchHabit();
  }, [habitId]);
  const handleSubmit = async data => {
    try {
      await API.put(`/habits/${habitId}`, data);
      navigate(`/habits/${habitId}`);
    } catch (err) {}
  };
  if (loading) return <LoadingSpinner />;
  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl p-6 border border-slate-100 dark:border-slate-700">
      <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-4">Edit Habit</h2>
      <HabitForm initialData={habit} onSubmit={handleSubmit} onCancel={() => navigate(-1)} />
    </div>
  );
};

export default HabitEdit;