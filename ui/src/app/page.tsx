'use client';

import Layout from '~/components/Layout';
import Section from '~/components/Section';
import Container from '~/components/Container';
import Map from '~/components/Map';
import Button from '~/components/Button';

import styles from '../styles/Home.module.scss';
const DEFAULT_CENTER = [38.907132, -77.036546]



export default function HomePage() {
  
  return (
    <div style={{
      height: '100vh',
      width: '100vw',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center'
    }}>
      <div style={{
        height: '80vh',
        width: '80vw',
        border: '1px solid black'
      }}>
      
          <Map className={styles.homeMap}  center={DEFAULT_CENTER} zoom={12}>
            {({ TileLayer, Marker, Popup }) => (
              <>
                <TileLayer
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                  attribution="&copy; <a href=&quot;http://osm.org/copyright&quot;>OpenStreetMap</a> contributors"
                />
                <Marker position={DEFAULT_CENTER}>
                  <Popup>
                    A pretty CSS3 popup. <br /> Easily customizable.
                  </Popup>
                </Marker>
              </>
            )}
          </Map>
        

      </div>
    </div>
  );
}