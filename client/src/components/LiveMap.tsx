import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
export function LiveMap({ miners }) {
  return (
    <MapContainer center={[32.0,53.0]} zoom={6} style={{ height: 500 }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {miners.map((m, i) =>
        m.lat && m.lon ? (
          <Marker key={i} position={[m.lat, m.lon]}>
            <Popup>
              IP: {m.ip}<br />
              پورت: {m.open_ports}<br />
              شهر: {m.city}<br />
              ریسک: {m.risk}
            </Popup>
          </Marker>
        ) : null
      )}
    </MapContainer>
  );
}