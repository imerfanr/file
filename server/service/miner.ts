import * as fs from "fs";
import * as ExcelJS from "exceljs";
export async function exportMiners(format: string, filter: string) {
  const miners = /* fetch filtered miners from DB */;
  if (format === "csv") {
    const csv = miners.map(m => `${m.ip},${m.open_ports},${m.city},${m.country}`).join("\n");
    fs.writeFileSync("/tmp/miners.csv", csv);
    return "/tmp/miners.csv";
  }
  if (format === "xlsx") {
    const wb = new ExcelJS.Workbook();
    // ... fill workbook
    await wb.xlsx.writeFile("/tmp/miners.xlsx");
    return "/tmp/miners.xlsx";
  }
  if (format === "json") {
    fs.writeFileSync("/tmp/miners.json", JSON.stringify(miners));
    return "/tmp/miners.json";
  }
}