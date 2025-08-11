import React, { useEffect, useRef } from 'react';
import { Finding } from '../types';
import NCWindow from './NCWindow';

declare const L: any; // Use Leaflet from CDN

interface MapViewerProps {
  findings: Finding[];
}

const MapViewer: React.FC<MapViewerProps> = ({ findings }) => {
  const mapRef = useRef<any>(null);
  const mapContainerRef = useRef<HTMLDivElement>(null);

  // Initialize map
  useEffect(() => {
    if (mapContainerRef.current && !mapRef.current) {
        mapRef.current = L.map(mapContainerRef.current, {
            center: [32.4279, 53.6880], // Center of Iran
            zoom: 5
        });

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(mapRef.current);
    }
  }, []);

  // Update markers when findings change
  useEffect(() => {
    if (!mapRef.current) return;

    // Clear existing markers
    mapRef.current.eachLayer((layer: any) => {
        if (layer instanceof L.Marker) {
            mapRef.current.removeLayer(layer);
        }
    });

    const locatedFindings = findings.filter(f => f.latitude && f.longitude);
    if (locatedFindings.length > 0) {
        const bounds = L.latLngBounds(
            locatedFindings.map(f => [f.latitude!, f.longitude!])
        );

        locatedFindings.forEach(finding => {
            const marker = L.marker([finding.latitude!, finding.longitude!])
                .addTo(mapRef.current);
            
            const popupContent = `
                <b>${finding.severity}: ${finding.description}</b><br>
                Target: ${finding.target}<br>
                <a href="https://www.google.com/maps?q=${finding.latitude},${finding.longitude}" target="_blank" rel="noopener noreferrer">Navigate</a>
            `;

            marker.bindPopup(popupContent);
        });

        mapRef.current.fitBounds(bounds, { padding: [50, 50] });
    }

  }, [findings]);


  return (
    <NCWindow title="Geographic Threat Map" style={{ flex: 1, width: '50%', minHeight: 0 }}>
        <div ref={mapContainerRef} style={{ flex: 1, width: '100%', height: '100%', backgroundColor: '#555555' }}>
            {/* Map will be rendered here by Leaflet */}
        </div>
    </NCWindow>
  );
};

export default MapViewer;
