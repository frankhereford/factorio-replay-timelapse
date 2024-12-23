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

  const changeTick = (step: number) => {
    const currentIndex = ticks.indexOf(selectedTick);
    const newIndex = Math.min(Math.max(currentIndex + step, 0), ticks.length - 1);
    if (ticks[newIndex] !== undefined) {
      onTickChange(ticks[newIndex]);
    }
  };

  const isMoveValid = (step: number) => {
    const currentIndex = ticks.indexOf(selectedTick);
    const newIndex = currentIndex + step;
    return newIndex >= 0 && newIndex < ticks.length;
  };

  const formatTick = (tick: number) => {
    const totalSeconds = tick / 60;
    const days = Math.floor(totalSeconds / (24 * 3600));
    const hours = Math.floor((totalSeconds % (24 * 3600)) / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = Math.floor(totalSeconds % 60);

    return `${days}d ${hours}h ${minutes}m ${seconds}s`;
  };

  return (
    <div className="absolute top-2 right-2 bg-white p-2 rounded shadow-lg z-50">
      <label htmlFor="tick-select" className="block text-sm font-medium text-gray-700">Select Tick:</label>
      <div className="flex items-center space-x-2">
        <button
          onClick={() => changeTick(-5)}
          className={`p-1 rounded ${isMoveValid(-5) ? 'bg-gray-200' : 'bg-gray-100 text-gray-400'}`}
          disabled={!isMoveValid(-5)}
        >
          {"<<"}
        </button>
        <button
          onClick={() => changeTick(-1)}
          className={`p-1 rounded ${isMoveValid(-1) ? 'bg-gray-200' : 'bg-gray-100 text-gray-400'}`}
          disabled={!isMoveValid(-1)}
        >
          {"<"}
        </button>
        <select
          id="tick-select"
          value={selectedTick}
          onChange={handleTickChange}
          className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
        >
          {ticks.map((tickValue) => (
            <option key={tickValue} value={tickValue}>
              {formatTick(tickValue)}
            </option>
          ))}
        </select>
        <button
          onClick={() => changeTick(1)}
          className={`p-1 rounded ${isMoveValid(1) ? 'bg-gray-200' : 'bg-gray-100 text-gray-400'}`}
          disabled={!isMoveValid(1)}
        >
          {">"}
        </button>
        <button
          onClick={() => changeTick(5)}
          className={`p-1 rounded ${isMoveValid(5) ? 'bg-gray-200' : 'bg-gray-100 text-gray-400'}`}
          disabled={!isMoveValid(5)}
        >
          {">>"}
        </button>
      </div>
    </div>
  );
};

export default TickPicker;