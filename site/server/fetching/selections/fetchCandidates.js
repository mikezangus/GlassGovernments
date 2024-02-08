const { getDB } = require("../../mongoClient");


module.exports = async function fetchCandidates({ year, office, state, district }) {
    try {
        const db = getDB();
        const collection = db.collection(`${year}_candidates`);
        const match = {
            OFFICE: office,
            STATE: state,
            DISTRICT: district
        };
        const lookup = {
            from: `${year}_contributions`,
            localField: "CAND_ID",
            foreignField: "CAND_ID",
            as: "contributions"
        };
        const unwind = {
            path: "$contributions",
            preserveNullAndEmptyArrays: true
        };
        const group = {
            _id: {
                name: "$NAME",
                party: "$PARTY",
                candID: "$CAND_ID"
            },
            totalContributionAmount: {
                $sum: "$contributions.TRAN_AMT"
            }
        };
        const projection = {
            _id: 0,
            candID: "$_id.candID",
            name: "$_id.name",
            party: "$_id.party",
            totalContributionAmount: 1
        };
        const pipeline = [
            { $match: match },
            { $lookup: lookup },
            { $unwind: unwind },
            { $group: group },
            { $project: projection }
        ];
        const data = await collection.aggregate(pipeline).toArray();
        return data;
    } catch (err) {
        console.error("Fetch Candidates | Error: ", err);
        throw err;
    };
};
