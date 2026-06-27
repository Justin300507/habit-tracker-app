import React, { useState, useEffect } from 'react';
import { Sun, Moon } from 'lucide-react';

const Header = () => {
  const [dark, setDark] = useState(false);
  useEffect(() => {
    document.documentElement.classList.toggle('dark', dark);
  }, [dark]);
  const today = new Date().toLocaleDateString(undefined, { weekday: 'long', month: 'short', day: 'numeric' });
  return (
    <header className="flex justify-between items-center mb-6">
      <h2 className="text-2xl font-semibold text-slate-900 dark:text-white">Hello, User! <span className="text-sm font-medium text-slate-500 dark:text-slate-400">-- {today}</span></h2>
      <button onClick={() => setDark(d => !d)} className="p-2 rounded-lg text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors">
        {dark ? <Sun size={18} /> : <Moon size={18} />}
      </button>
    </header>
  );
};

export default Header;