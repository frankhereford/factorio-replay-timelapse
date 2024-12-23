import React from 'react';

interface TickPickerProps {
  ticks: number[];
  selectedTick: number;
  onTickChange: (tick: number) => void;
}

const TickPicker: React.FC<TickPickerProps> = ({ ticks, selectedTick, onTickChange }) => {
  const handleTickChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    onTickChange(Number(event.target.value));
  };

  const formatTickToHumanTime = (tick: number) => {
    const totalSeconds = tick / 60;
    const days = Math.floor(totalSeconds / (24 * 3600));
    const hours = Math.floor((totalSeconds % (24 * 3600)) / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = Math.floor(totalSeconds % 60);

    return `${days > 0 ? days + 'd ' : ''}${hours > 0 ? hours + 'h ' : ''}${minutes > 0 ? minutes + 'm ' : ''}${seconds}s`;
  };

  return (
    <div className="absolute top-2 right-2 bg-white p-2 rounded shadow-lg z-50">
      <label htmlFor="tick-select" className="block text-sm font-medium text-gray-700">Select Time:</label>
      <select id="tick-select" value={selectedTick} onChange={handleTickChange} className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md">
        {ticks.map((tickValue) => (
          <option key={tickValue} value={tickValue}>
            {formatTickToHumanTime(tickValue)}
          </option>
        ))}
      </select>
    </div>
  );
};

export default TickPicker;