import React from 'react';
import { Loader } from 'lucide-react';

const LoadingSpinner = () => (
  <div className="flex justify-center items-center py-4">
    <Loader size={24} className="animate-spin text-indigo-600" />
  </div>
);

export default LoadingSpinner;