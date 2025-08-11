import { getMiners } from "../service/miner";
import { toCsv, toExcel, toJson } from "../lib/export";
export default async function handler(req, res) {
  const miners = await getMiners();
  const { format = "csv" } = req.query;
  if (format === "csv") return res.send(toCsv(miners));
  if (format === "xlsx") return res.sendFile(await toExcel(miners));
  if (format === "json") return res.json(toJson(miners));
}