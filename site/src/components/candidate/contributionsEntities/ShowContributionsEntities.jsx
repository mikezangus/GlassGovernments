import { useState } from "react";
import useFetchEntities from "./useFetchContributionsEntities";
import RenderContributionsEntities from "./RenderContributionsEntities";


export default function ShowEntities({ year, candidate }) {
    const { totalContributionAmount, candID, name, party } = candidate;
    const [entities, setEntities] = useState([]);
    useFetchEntities(year, candID, setEntities);
    return (
        <RenderContributionsEntities
            totalContributionAmount={totalContributionAmount}
            entities={entities}
        />
    );
};