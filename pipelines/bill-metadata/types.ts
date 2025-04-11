export type RawBill = {
    congress: string;
    type: string;
    number: number;
    title: string;
};


export type Bill = {
    id: string;
    congress: number;
    type: string;
    num: number;
    title: string,
    h_vote: number;
    h_year: number;
    s_vote: number;
    s_session: number;
};
