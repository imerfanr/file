import nodemailer from "nodemailer";
import { sendTelegram } from "./telegram";
export async function notify(miner) {
  await transporter.sendMail({
    to: "security@example.com", subject: "هشدار ماینر", text: JSON.stringify(miner)
  });
  await sendTelegram(`ماینر مشکوک شناسایی شد: ${miner.ip}`);
}