import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Button from '../components/Button';
import LoadingSpinner from '../components/LoadingSpinner';
import API from '../api';
import StreakBadge from '../components/StreakBadge';

const HabitDetail = () => {
  const { habitId } = useParams();
  const [habit, setHabit] = useState(null);
  const [loading, setLoading] = useState(true);
  const [logging, setLogging] = useState(false);
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
  const handleLog = async () => {
    setLogging(true);
    try {
      await API.post(`/habits/${habitId}/log`);
      const res = await API.get(`/habits/${habitId}`);
      setHabit(res.data);
    } catch (err) {}
    setLogging(false);
  };
  if (loading) return <LoadingSpinner />;
  if (!habit) return <p className="text-slate-500 dark:text-slate-400">Habit not found.</p>;
  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl p-6 border border-slate-100 dark:border-slate-700">
      <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-2">{habit.name}</h2>
      <p className="text-slate-500 dark:text-slate-400 mb-4">{habit.description}</p>
      <StreakBadge streak={habit.streak} />
      <div className="mt-4">
        <Button onClick={handleLog} disabled={logging}>
          {logging ? 'Logging...' : 'Mark Today Completed'}
        </Button>
      </div>
    </div>
  );
};

export default HabitDetail;