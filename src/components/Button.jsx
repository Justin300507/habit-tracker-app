import React from 'react';

const Button = ({ children, onClick, type = 'button', className = '' }) => (
  <button type={type} onClick={onClick} className={`bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded ${className}`}>
    {children}
  </button>
);

export default Button;