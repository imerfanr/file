import { useEffect, useState } from "react";
export function Notifications() {
  const [alerts, setAlerts] = useState([]);
  useEffect(() => {
    const ws = new WebSocket("ws://localhost:3301/alerts");
    ws.onmessage = e => setAlerts(prev => [JSON.parse(e.data), ...prev]);
    return () => ws.close();
  }, []);
  return (
    <div className="fixed top-2 right-2 z-50">
      {alerts.map((a, i) => (
        <div key={i} className="bg-red-600 text-white px-4 py-2 my-2 rounded shadow-lg animate-bounce">
          ⚠️ {a.message}
        </div>
      ))}
    </div>
  );
}