const { getDB } = require("../src/lib/mongoClient");


async function createIndexes(years) {
    console.log("entered create indexes")
    const db = getDB();
    for (const year of years) {
        try {
            await db
                .collection(`${year}_candidates`)
                .createIndex({
                    OFFICE: 1,
                    STATE: 1,
                    DISTRICT: 1
                });
            console.log("Successfully created index 1");
            await db
                .collection(`${year}_candidates`)
                .createIndex({
                    CAND_ID: 1
                });
            console.log("Successfully created index 2");
            await db
                .collection(`${year}_contributions`)
                .createIndex({
                    CAND_ID: 1
                });
            console.log("Successfully created index 3");
        } catch (err) {
            console.error("Error creating indexes:", err);
        };
    };
};


module.exports = createIndexes;
