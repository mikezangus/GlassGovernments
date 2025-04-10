import { Bill, RawBill } from "../types";


export default function createRow(data: RawBill[]): Bill[]
{
    return data.map((item) => {
        const id = `${item.congress}_${item.type}_${item.number}`;
        const congress = Number(item.congress);
        return {
            id,
            congress: congress,
            type: item.type,
            num: item.number,
            action: false
        }
    });
}
