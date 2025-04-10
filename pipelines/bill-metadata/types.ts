export type RawBill = {
    congress: string;
    type: string;
    number: string;
};


export type Bill = {
    id: string;
    congress: number;
    type: string;
    num: string;
    action: boolean;
};
