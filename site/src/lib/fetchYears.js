export default async function fetchYears(db) {
    try {

        let uniqueYears = new Set();
        const collections = await db
            .listCollections()
            .toArray();
        const candidateCollections = collections.filter(
            col => col.name.endsWith("cands")
        );
        for (let collection of candidateCollections) {
            let years = await db
                .collection(collection.name)
                .aggregate([
                    { $match: { YEAR: { $exists: true } } },
                    { $group: { _id: "$YEAR" } }
                ]).toArray();
            years.forEach(
                yearDoc => uniqueYears.add(yearDoc._id)
            );
        }
        const data = Array
            .from(uniqueYears)
            .filter(year => year != null)
            .map(String)
        return data
    } catch (err) {
        console.error("Fetch Years | Error: ", err);
        throw new Error("Fetch Yeras | Failed");
    }
};
