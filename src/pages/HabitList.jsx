import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import HabitCard from '../components/HabitCard';
import Button from '../components/Button';
import LoadingSpinner from '../components/LoadingSpinner';
import API from '../api';

const HabitList = () => {
  const [habits, setHabits] = useState([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    const fetchHabits = async () => {
      try {
        const res = await API.get('/habits');
        setHabits(res.data);
      } catch (err) {}
      setLoading(false);
    };
    fetchHabits();
  }, []);
  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-semibold text-slate-900 dark:text-white">Habits</h2>
        <Link to="/habits/new">
          <Button className="bg-indigo-600 hover:bg-indigo-700">Add Habit</Button>
        </Link>
      </div>
      {loading ? <LoadingSpinner /> : habits.length ? habits.map(h => <HabitCard key={h.id} habit={h} />) : <p className="text-slate-500 dark:text-slate-400">No habits found.</p>}
    </div>
  );
};

export default HabitList;