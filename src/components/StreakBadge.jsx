import React from 'react';

const StreakBadge = ({ streak }) => (
  <span className="badge bg-indigo-50 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-400">
    {streak} day{streak === 1 ? '' : 's'}
  </span>
);

export default StreakBadge;