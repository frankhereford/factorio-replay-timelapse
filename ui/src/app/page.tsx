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
      <Map className={styles.homeMap} center={DEFAULT_CENTER} zoom={10} minZoom={7} maxZoom={13}>
        {({ TileLayer, Marker, Popup }: { TileLayer: any; Marker: any; Popup: any }) => (
          <>
            <TileLayer
              url="http://fjord:9000/30000/{z}/{x}/{y}.png"
              tileSize={1024}
            />
            <Marker position={DEFAULT_CENTER} />
          </>
        )}
      </Map>
    </div>
  );
}