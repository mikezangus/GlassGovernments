export const tableName = "votes";


export const schema = `
    bill_id varchar(15) NOT NULL,
    bio_id char(7) NOT NULL,
    vote char(1) NOT NULL,
    chamber char(1) NOT NULL,
    PRIMARY KEY (bill_id, bio_id)
`;
