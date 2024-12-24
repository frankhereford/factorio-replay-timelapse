import React from 'react';
import { Scrubber } from 'react-scrubber';
import 'react-scrubber/lib/scrubber.css';

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

  const handleScrubChange = (value: number) => {
    const tickIndex = Math.round(value); // Ensure we select the closest tick
    if (tickIndex >= 0 && tickIndex < ticks.length) {
      const tick = ticks[tickIndex];
      if (tick !== undefined) {
        onTickChange(tick);
      }
    }
  };

  const handlePreviousTick = () => {
    const currentIndex = ticks.indexOf(selectedTick);
    if (currentIndex > 0) {
      const previousTick = ticks[currentIndex - 1];
      if (previousTick !== undefined) {
        onTickChange(previousTick);
      }
    }
  };

  const handleNextTick = () => {
    const currentIndex = ticks.indexOf(selectedTick);
    if (currentIndex < ticks.length - 1) {
      const nextTick = ticks[currentIndex + 1];
      if (nextTick !== undefined) {
        onTickChange(nextTick);
      }
    }
  };

  const handlePrevious15Ticks = () => {
    const currentIndex = ticks.indexOf(selectedTick);
    if (currentIndex >= 15) {
      const previousTick = ticks[currentIndex - 15];
      if (previousTick !== undefined) {
        onTickChange(previousTick);
      }
    }
  };

  const handleNext15Ticks = () => {
    const currentIndex = ticks.indexOf(selectedTick);
    if (currentIndex <= ticks.length - 16) {
      const nextTick = ticks[currentIndex + 15];
      if (nextTick !== undefined) {
        onTickChange(nextTick);
      }
    }
  };

  return (
    <div className="absolute top-10 right-10 w-1/3 bg-white bg-opacity-50 backdrop-blur-sm p-4 rounded-lg shadow-lg">
      <div className="p-0 flex items-center">
        <button
          onClick={handlePrevious15Ticks}
          disabled={ticks.indexOf(selectedTick) < 15}
          className="mr-2 p-2 bg-gray-200 rounded disabled:bg-gray-400"
        >
          &larr;&larr;
        </button>
        <button
          onClick={handlePreviousTick}
          disabled={ticks.indexOf(selectedTick) === 0}
          className="mr-2 p-2 bg-gray-200 rounded disabled:bg-gray-400"
        >
          &larr;
        </button>
        <div className="flex-grow text-center">{formatTick(selectedTick)}</div>
        <button
          onClick={handleNextTick}
          disabled={ticks.indexOf(selectedTick) === ticks.length - 1}
          className="ml-2 p-2 bg-gray-200 rounded disabled:bg-gray-400"
        >
          &rarr;
        </button>
        <button
          onClick={handleNext15Ticks}
          disabled={ticks.indexOf(selectedTick) > ticks.length - 16}
          className="ml-2 p-2 bg-gray-200 rounded disabled:bg-gray-400"
        >
          &rarr;&rarr;
        </button>
      </div>
      <div className="p-0">
        <Scrubber
          min={0}
          max={ticks.length - 1}
          value={ticks.indexOf(selectedTick)}
          onScrubChange={handleScrubChange}
          className="w-full mt-2"
        />
      </div>
    </div>
  );
};

export default TickPicker;