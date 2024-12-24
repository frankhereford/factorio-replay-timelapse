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

  return (
      <div className="absolute top-10 right-10 w-1/3 bg-white bg-opacity-50 backdrop-blur-sm p-4 rounded-lg shadow-lg">
        <div className="p-0">
          <Scrubber
            min={0}
            max={ticks.length - 1}
            value={ticks.indexOf(selectedTick)}
            onScrubChange={handleScrubChange}
            // tooltip={{
            //   enabledOnHover: true,
            //   enabledOnScrub: true,
            //   formatString: (value: number) => formatTick(ticks[Math.round(value)] || 0),
            // }}
            className="w-full mt-2"
          />
          <div className="mt-1 text-center">{formatTick(selectedTick)}</div>
        </div>
      </div>
    );
  };
export default TickPicker;
