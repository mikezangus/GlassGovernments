import { useState } from "react";
import useFetchEntities from "./useFetchContributionsEntities";
import RenderContributionsEntities from "./RenderContributionsEntities";


export default function ShowEntities({ chamber, state, district, candidate }) {
    const [entities, setEntities] = useState([]);
    useFetchEntities(chamber, state, district, candidate, setEntities);
    return (
        <RenderContributionsEntities
            candidate={candidate}
            entities={entities}
        />
    );
};