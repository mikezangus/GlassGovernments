const { getDB } = require("../mongoClient");


module.exports = async function fetchStates({ year, office }) {
    try {
        const db = getDB();
        const collection = db.collection(`${year}_candidates`);
        const states = await collection.distinct(
            "STATE", { OFFICE: office }
        );
        return states;
    } catch (err) {
        console.error("Fetch States | Error: ", err);
        throw err;
    };
};
