import { useState } from "react";
import useFetchEntities from "./useFetchEntities";
import RenderEntities from "./RenderEntities";


export default function ShowEntities({ chamber, state, district, candidate }) {
    const [entities, setEntities] = useState([]);
    useFetchEntities(chamber, state, district, candidate, setEntities);
    return (
        <RenderEntities
            candidate={candidate}
            entities={entities}
        />
    );
};