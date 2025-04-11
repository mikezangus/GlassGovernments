export type RawBill = {
    congress: string;
    type: string;
    number: string;
    title: string;
};


export type Bill = {
    id: string;
    congress: number;
    type: string;
    num: string;
    title: string,
    action: boolean;
};
