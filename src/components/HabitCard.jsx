import React from 'react';
import { CheckSquare, Calendar } from 'lucide-react';
import { Link } from 'react-router-dom';
import StreakBadge from './StreakBadge';

const HabitCard = ({ habit }) => (
  <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-100 dark:border-slate-700 p-4 flex items-center justify-between hover:shadow-sm transition-shadow">
    <div className="flex items-center gap-3">
      <div className="w-9 h-9 rounded-lg bg-indigo-50 dark:bg-indigo-900/30 flex items-center justify-center">
        <CheckSquare size={18} className="text-indigo-600 dark:text-indigo-400" />
      </div>
      <div>
        <p className="text-sm font-semibold text-slate-900 dark:text-white">{habit.title}</p>
        <p className="text-xs text-slate-500 dark:text-slate-400">{habit.description}</p>
      </div>
    </div>
    <div className="flex items-center gap-2">
      <StreakBadge streak={habit.current_streak || 0} />
      <Link to={`/habits/${habit.id}`} className="text-indigo-600 dark:text-indigo-400 hover:underline flex items-center gap-1">
        <Calendar size={14} /> Details
      </Link>
    </div>
  </div>
);

export default HabitCard;