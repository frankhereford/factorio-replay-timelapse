import React from 'react';

interface SurfaceSelectorProps {
  selectedSurface: string;
  onSurfaceChange: (surface: string) => void;
  surfaces: string[];
}

const SurfaceSelector: React.FC<SurfaceSelectorProps> = ({ selectedSurface, onSurfaceChange, surfaces }) => {
  return (
    <div className="absolute top-10 left-10 w-1/3 bg-white bg-opacity-50 backdrop-blur-sm p-4 rounded-lg shadow-lg">
      <label className="block mb-2 text-sm font-medium text-gray-700">Select Surface:</label>
      <select
        value={selectedSurface}
        onChange={(e) => onSurfaceChange(e.target.value)}
        className="block w-full p-2 border border-gray-300 rounded"
      >
        {surfaces.map((surface) => (
          <option key={surface} value={surface}>
            {surface}
          </option>
        ))}
      </select>
    </div>
  );
};

export default SurfaceSelector;