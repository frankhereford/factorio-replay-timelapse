'use client';

import Layout from '~/components/Layout';
import Section from '~/components/Section';
import Container from '~/components/Container';
import Map from '~/components/Map';
import Button from '~/components/Button';

import styles from '../styles/Home.module.scss';

const DEFAULT_CENTER = [0,0]

export default function HomePage() {
  return (
    <div className={styles.mapContainer}>
      <Map className={styles.homeMap} center={DEFAULT_CENTER} zoom={6} minZoom={3} maxZoom={8}>
        {({ TileLayer, Marker, Popup }: { TileLayer: any; Marker: any; Popup: any }) => (
          <>
            <TileLayer
              url="http://fjord:9000/stills/1050000/{z}/{x}/{y}.png"
              tileSize={256}
            />
            <TileLayer
              url="http://fjord:9000/debug/{z}/{x}/{y}.png"
              tileSize={256}
            />
            <Marker position={DEFAULT_CENTER} />
          </>
        )}
      </Map>
    </div>
  );
}