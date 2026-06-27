import React from 'react';

const Input = ({ label, type = 'text', value, onChange, placeholder, required }) => (
  <div className="space-y-1">
    <label className="text-xs font-medium text-slate-700 dark:text-slate-300">{label}</label>
    <input
      type={type}
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      required={required}
      className="input"
    />
  </div>
);

export default Input;