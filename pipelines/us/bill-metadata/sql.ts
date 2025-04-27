export const tableName = "bill_metadata";


export const schema = `
    id VARCHAR(15) PRIMARY KEY,
    congress SMALLINT,
    type VARCHAR(7),
    num INTEGER,
    h_vote INTEGER,
    h_year INTEGER,
    s_vote iNTEGER,
    s_session INTEGER,
    title TEXT
`;
