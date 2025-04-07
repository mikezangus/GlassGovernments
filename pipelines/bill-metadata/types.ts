import { FieldPacket, RowDataPacket } from "mysql2/promise";


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
    action: number;
};


export type MySQLResponse = [
    RowDataPacket[],
    FieldPacket[]
];
