import { BillMetadata } from "../types";


export default function populateFields(bill: BillMetadata, votes: any[]): void
{
    for (const vote of votes) {
        if (vote.chamber === "House" && vote.date && vote.rollNumber) {
            bill.h_year = vote.date.slice(0, 4);
            bill.h_vote = vote.rollNumber;
        } else if (vote.chamber === "Senate" && vote.rollNumber && vote.sessionNumber) {
            bill.s_vote = vote.rollNumber;
            bill.s_session = vote.sessionNumber;
        }
    }
}
