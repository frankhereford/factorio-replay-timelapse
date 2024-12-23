'use client';

import React, { useState } from 'react';
import Layout from '~/components/Layout';
import Section from '~/components/Section';
import Container from '~/components/Container';
import Map from '~/components/Map';
import Button from '~/components/Button';

import styles from '../styles/Home.module.scss';

const DEFAULT_CENTER = [0,0];

const jump = 15000;
const end = 1200000;

export default function HomePage() {
  const [selectedValue, setSelectedValue] = useState(0);

  const handleDropdownChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedValue(Number(event.target.value));
  };

  const handleIncrement = () => {
    setSelectedValue(prev => Math.min(prev + jump, end));
  };

  const handleDecrement = () => {
    setSelectedValue(prev => Math.max(prev - jump, 0));
  };

  const dropdownValues = Array.from({ length: 41 }, (_, i) => i * jump);

  return (
    <div className={styles.mapContainer}>
      <div className={styles.dropdownContainer}>
        <button onClick={handleDecrement} disabled={selectedValue === 0}>
          &uarr;
        </button>
        <select onChange={handleDropdownChange} value={selectedValue}>
          {dropdownValues.map(value => (
            <option key={value} value={value}>
              n = {value}
            </option>
          ))}
        </select>
        <button onClick={handleIncrement} disabled={selectedValue === end}>
          &darr;
        </button>
      </div>
      <Map className={styles.homeMap} center={DEFAULT_CENTER} zoom={6} minZoom={0} maxZoom={14}>
        {({ TileLayer, Marker, Popup }: { TileLayer: any; Marker: any; Popup: any }) => (
          <>
            <TileLayer
              url={`http://fjord:9000/stills/${selectedValue}/{z}/{x}/{y}.png`}
              tileSize={256}
            />
            {/* <TileLayer
              url="http://fjord:9000/debug/{z}/{x}/{y}.png"
              tileSize={256}
            /> */}
            <Marker position={DEFAULT_CENTER} />
          </>
        )}
      </Map>
    </div>
  );
}