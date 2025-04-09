export const tableName = "bill_metadata";


export const schema = `
    id VARCHAR(15) PRIMARY KEY,
    congress SMALLINT,
    type VARCHAR(7),
    num VARCHAR(5),
    action BOOLEAN DEFAULT FALSE
`;
