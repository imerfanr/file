import { WebSocketServer } from "ws";
import { getAllMiners } from "../service/miner";
const wss = new WebSocketServer({ port: 3301 });
wss.on("connection", ws => {
  setInterval(async () => {
    const miners = await getAllMiners();
    ws.send(JSON.stringify(miners));
  }, 5000);
});
export default wss;