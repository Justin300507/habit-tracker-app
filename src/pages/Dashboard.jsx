import React, { useState, useEffect } from 'react';
import DashboardChart from '../components/DashboardChart';
import HabitCard from '../components/HabitCard';
import LoadingSpinner from '../components/LoadingSpinner';
import API from '../api';

const Dashboard = () => {
  const [stats, setStats] = useState({});
  const [recent, setRecent] = useState([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    const fetchData = async () => {
      try {
        const resStats = await API.get('/dashboard/weekly');
        setStats(resStats.data);
        const resRecent = await API.get('/habits');
        setRecent(resRecent.data.slice(0,5));
      } catch (err) {}
      setLoading(false);
    };
    fetchData();
  }, []);
  const statCards = [
    { label: 'Total Habits', value: stats.totalHabits || 0, change: '+5% this week' },
    { label: 'Active Streak', value: stats.activeStreak || 0, change: '+2% this week' },
    { label: 'Completed Today', value: stats.completedToday || 0, change: '+10% this week' },
    { label: 'Overall Completion', value: stats.overallCompletion ? `${stats.overallCompletion}%` : '0%', change: '' },
  ];
  return (
    <div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {statCards.map((c, i) => (
          <div key={i} className="bg-white dark:bg-slate-800 rounded-xl p-5 border border-slate-100 dark:border-slate-700 shadow-sm">
            <p className="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wide">{c.label}</p>
            <p className="text-2xl font-bold text-slate-900 dark:text-white mt-1">{c.value}</p>
            {c.change && <p className="text-xs text-indigo-600 mt-1">{c.change}</p>}
          </div>
        ))}
      </div>
      <DashboardChart data={stats.weeklyData || []} />
      <h3 className="font-semibold text-slate-900 dark:text-white mt-6 mb-4">Recent Habits</h3>
      {loading ? <LoadingSpinner /> : recent.length ? recent.map(h => <HabitCard key={h.id} habit={h} />) : <p className="text-slate-500 dark:text-slate-400">No recent habits.</p>}
    </div>
  );
};

export default Dashboard;