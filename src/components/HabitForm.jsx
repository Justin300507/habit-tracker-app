import React, { useState } from 'react';
import Input from './Input';
import Button from './Button';

const HabitForm = ({ initialData = {}, onSubmit, onCancel }) => {
  const [name, setName] = useState(initialData.name || '');
  const [description, setDescription] = useState(initialData.description || '');
  const [isActive, setIsActive] = useState(initialData.is_active ?? true);
  const handleSubmit = e => {
    e.preventDefault();
    onSubmit({ name, description, is_active: isActive });
  };
  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input label="Name" value={name} onChange={e => setName(e.target.value)} placeholder="Habit name" />
      <Input label="Description" value={description} onChange={e => setDescription(e.target.value)} placeholder="Optional description" />
      <div className="flex items-center">
        <input id="active" type="checkbox" checked={isActive} onChange={e => setIsActive(e.target.checked)} className="form-checkbox h-4 w-4 text-indigo-600 border-slate-300 rounded" />
        <label htmlFor="active" className="ml-2 text-sm text-slate-700 dark:text-slate-300">Active</label>
      </div>
      <div className="flex gap-2">
        <Button type="submit">Save</Button>
        {onCancel && <Button type="button" onClick={onCancel} className="bg-slate-200 hover:bg-slate-300 text-slate-800">Cancel</Button>}
      </div>
    </form>
  );
};

export default HabitForm;