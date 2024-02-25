import { useState } from "react";
import useFetchEntities from "./useFetchContributionsEntities";
import RenderContributionsEntities from "./RenderContributionsEntities";


export default function ContributionsEntities({ year, candidate }) {
    const { totalContAmt, candID } = candidate;
    const [entities, setEntities] = useState([]);
    useFetchEntities(year, candID, setEntities);
    return (
        <RenderContributionsEntities
            totalContAmt={totalContAmt}
            entities={entities}
        />
    );
};
