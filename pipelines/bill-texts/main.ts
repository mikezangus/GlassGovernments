import fetchFromFiles from "./fetchFromFiles";
import insertToDB from "./insertToDB";


async function main()
{
    const data = await fetchFromFiles();
    await insertToDB(data);
}


if (require.main === module) {
    main();
}
