export type RawBillMetadata = {
    congress: string;
    type: string;
    number: number;
    title: string;
};


export type BillMetadata = {
    id: string;
    congress: number;
    type: string;
    num: number;
    h_vote: number;
    h_year: number;
    s_vote: number;
    s_session: number;
    title: string,
};
