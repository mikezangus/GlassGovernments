export const tableName = "BillMetadata";


export const schema = `
    id VARCHAR(15) PRIMARY KEY,
    congress TINYINT,
    type VARCHAR(7),
    num VARCHAR(5),
    action TINYINT(1) DEFAULT 0
`;
