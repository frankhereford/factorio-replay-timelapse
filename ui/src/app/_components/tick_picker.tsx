import React from 'react';

interface TickPickerProps {
  ticks: number[];
  selectedTick: number;
  onTickChange: (tick: number) => void;
}

const TickPicker: React.FC<TickPickerProps> = ({ ticks, selectedTick, onTickChange }) => {
  const formatTick = (tick: number) => {
    const totalSeconds = tick / 60;
    const days = Math.floor(totalSeconds / (24 * 3600));
    const hours = Math.floor((totalSeconds % (24 * 3600)) / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = Math.floor(totalSeconds % 60);

    return `${days}d ${hours}h ${minutes}m ${seconds}s`;
  };

  const handleSliderChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const tickIndex = Number(event.target.value);
    if (tickIndex >= 0 && tickIndex < ticks.length) {
      const tick = ticks[tickIndex];
      if (tick !== undefined) {
        onTickChange(tick);
      }
    }
  };

  return (
    <div className="p-2">
      {/* <label className="block text-sm font-medium text-gray-700">Select Tick:</label> */}
      <input
        type="range"
        min={0}
        max={ticks.length - 1}
        value={ticks.indexOf(selectedTick)}
        onChange={handleSliderChange}
        className="w-full mt-1"
      />
      <div className="mt-1 text-center">{formatTick(selectedTick)}</div>
    </div>
  );
};

export default TickPicker;