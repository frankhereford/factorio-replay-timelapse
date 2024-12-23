'use client';

import React, { useState } from 'react';

const jump = 15000;
const end = 1200000;

interface TickPickerProps {
  selectedValue: number;
  onChange: (value: number) => void;
}

const TickPicker: React.FC<TickPickerProps> = ({ selectedValue, onChange }) => {
  const handleDropdownChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    onChange(Number(event.target.value));
  };

  const handleIncrement = () => {
    onChange(Math.min(selectedValue + jump, end));
  };

  const handleDecrement = () => {
    onChange(Math.max(selectedValue - jump, 0));
  };

  const dropdownValues = Array.from({ length: 82 }, (_, i) => i * jump);

  return (
    <div className="flex items-center space-x-2">
      <button
        onClick={handleDecrement}
        disabled={selectedValue === 0}
        className="px-2 py-1 bg-gray-200 rounded disabled:opacity-50"
      >
        &uarr;
      </button>
      <select
        onChange={handleDropdownChange}
        value={selectedValue}
        className="px-2 py-1 border rounded"
      >
        {dropdownValues.map(value => (
          <option key={value} value={value}>
            n = {value}
          </option>
        ))}
      </select>
      <button
        onClick={handleIncrement}
        disabled={selectedValue === end}
        className="px-2 py-1 bg-gray-200 rounded disabled:opacity-50"
      >
        &darr;
      </button>
    </div>
  );
};

export default TickPicker;