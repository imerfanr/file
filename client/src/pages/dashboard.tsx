import dynamic from "next/dynamic";
import { useEffect, useState } from "react";
const Map = dynamic(() => import("@/components/LiveMap"), { ssr: false });
import { Table } from "@/components/Table";
import { PieChart, BarChart } from "recharts";
export default function Dashboard() {
  const [miners, setMiners] = useState([]);
  useEffect(() => {
    const ws = new WebSocket("ws://localhost:3301");
    ws.onmessage = e => setMiners(JSON.parse(e.data));
    return () => ws.close();
  }, []);
  return (
    <div className="grid grid-cols-2 gap-6">
      <Map miners={miners} />
      <Table data={miners} />
      <PieChart data={miners} /* ... */ />
      <BarChart data={miners} /* ... */ />
    </div>
  );
}