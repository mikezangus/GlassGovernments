import { Bill, RawBill } from "../types";


export default function process(input: RawBill[]): Bill[]
{
    return input.map((item) => {
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
