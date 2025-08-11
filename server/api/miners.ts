import express from "express";
import { getAllMiners, startScan, exportMiners, updateRules } from "../service/miner";
const router = express.Router();

router.get("/", async (_req, res) => {
  const miners = await getAllMiners();
  res.json(miners);
});

router.post("/scan", async (req, res) => {
  await startScan(req.body); // اجرای python worker
  res.json({ message: "Scan started" });
});

router.get("/export", async (req, res) => {
  const { format = "csv" } = req.query;
  const file = await exportMiners(format as string);
  res.download(file);
});

router.post("/rules", async (req, res) => {
  await updateRules(req.body);
  res.json({ message: "Rules updated" });
});
export default router;