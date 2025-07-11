import fs from "fs";


export default function log(message: string): void
{
    const timestamp = new Date().toLocaleString();
    const entry = `[${timestamp}] ${message}\n`;
    fs.appendFileSync("log.log", entry, "utf8");
}
