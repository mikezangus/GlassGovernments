import { useState } from "react";
import useFetchEntities from "./EntitiesFetcher";
import RenderEntities from "./EntitiesRenderer";


export default function ShowEntities({ chamber, state, district, candidate }) {
    const [entityContributions, setEntityContributions] = useState([]);
    useFetchEntities(chamber, state, district, candidate, setEntityContributions);
    return RenderEntities(candidate, entityContributions);
};