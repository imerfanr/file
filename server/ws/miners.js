const wsClients = new Set();
function broadcastMiners(miners) {
  wsClients.forEach((ws) => {
    try { ws.send(JSON.stringify(miners)); } catch {}
  });
}
app.ws("/ws/miners", (ws, req) => {
  wsClients.add(ws);
  ws.on("close", () => wsClients.delete(ws));
});
module.exports = { broadcastMiners };