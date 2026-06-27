import React from 'react';
import { useNavigate } from 'react-router-dom';
import HabitForm from '../components/HabitForm';
import API from '../api';

const HabitNew = () => {
  const navigate = useNavigate();
  const handleSubmit = async data => {
    try {
      const res = await API.post('/habits', data);
      navigate(`/habits/${res.data.id}`);
    } catch (err) {}
  };
  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl p-6 border border-slate-100 dark:border-slate-700">
      <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-4">New Habit</h2>
      <HabitForm onSubmit={handleSubmit} onCancel={() => navigate('/habits')} />
    </div>
  );
};

export default HabitNew;
