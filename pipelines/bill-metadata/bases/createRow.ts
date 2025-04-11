import { RawBill, Bill } from "../types";


export default function createRow(data: RawBill[]): Bill[]
{
    return data
        .filter(item => item.congress && item.type && item.number)
        .map((item) => {
            const id = `${item.congress}_${item.type}_${item.number}`;
            const congress = Number(item.congress);
            return {
                id,
                congress: congress,
                type: item.type,
                num: item.number,
                title: item.title,
                h_vote: 0,
                h_year: 0,
                s_vote: 0,
                s_session: 0
            }
        }
    );
}
