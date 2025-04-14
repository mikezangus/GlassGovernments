import fs from "fs/promises";
import path from "path";
import { BillText } from "../types";


const DIR = path.resolve(__dirname, "../../data/bill-texts");


export default async function loadFromFiles(): Promise<BillText[]>
{
    const data: BillText[] = [];
    const fileNames = await fs.readdir(DIR);
    for (const fileName of fileNames) {
        try {
            console.log(fileName);
            const filePath = path.join(DIR, fileName);
            const stat = await fs.stat(filePath);
            if (!stat.isFile()
                || fileName.startsWith(".")
                || !fileName.endsWith(".txt")
            ) {
                continue;
            }
            const id = path.parse(fileName).name;
            const text = await fs.readFile(filePath, "utf-8");
            data.push({ id, text });
        } catch (err) {
            console.error(`Error fetching file ${fileName}:\n${err}`);
        }
    }
    return data;
}
