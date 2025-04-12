import loadFromFiles from "./loadFromFiles";
import insertToDB from "./insertToDB";


async function main()
{
    const data = await loadFromFiles();
    await insertToDB(data);
}


if (require.main === module) {
    main();
}
