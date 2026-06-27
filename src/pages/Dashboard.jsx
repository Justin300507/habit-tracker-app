import React, { useState, useEffect } from 'react';
import DashboardChart from '../components/DashboardChart';
import HabitCard from '../components/HabitCard';
import LoadingSpinner from '../components/LoadingSpinner';
import API from '../api';

const Dashboard = () => {
  const [items, setItems] = useState([]);
  const [recent, setRecent] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const resHabits = await API.get('/habits');
        setRecent((resHabits.data.items || []).slice(0, 5));
      } catch (err) {}
      try {
        const resStats = await API.get('/dashboard/weekly');
        setItems(resStats.data.items || []);
      } catch (err) {}
      setLoading(false);
    };
    fetchData();
  }, []);

  const totalHabits = items.length;
  const activeStreak = items.length ? Math.max(...items.map(i => i.streak || 0)) : 0;
  const overallCompletion = items.length
    ? Math.round(items.reduce((s, i) => s + (i.weekly_completion || 0), 0) / items.length)
    : 0;

  const statCards = [
    { label: 'Total Habits', value: totalHabits },
    { label: 'Best Streak', value: `${activeStreak} days` },
    { label: 'Weekly Completion', value: `${overallCompletion}%` },
  ];

  return (
    <div>
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
        {statCards.map((c, i) => (
          <div key={i} className="bg-white dark:bg-slate-800 rounded-xl p-5 border border-slate-100 dark:border-slate-700 shadow-sm">
            <p className="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wide">{c.label}</p>
            <p className="text-2xl font-bold text-slate-900 dark:text-white mt-1">{c.value}</p>
          </div>
        ))}
      </div>
      <DashboardChart data={items} />
      <h3 className="font-semibold text-slate-900 dark:text-white mt-6 mb-4">Recent Habits</h3>
      {loading ? <LoadingSpinner /> : recent.length ? recent.map(h => <HabitCard key={h.id} habit={h} />) : <p className="text-slate-500 dark:text-slate-400">No habits yet. <a href="/habits" className="text-indigo-600 hover:underline">Add one</a>.</p>}
    </div>
  );
};

export default Dashboard;
