import { useState } from "react";
import useFetchCoordinates from "./useFetchCoordinates";
import RenderMap from "./RenderMap";


export default function ShowMap({ chamber, state, district, candidate }) {
    const [coordinates, setCoordinates] = useState([]);
    useFetchCoordinates(chamber, state, district, candidate, setCoordinates);
    return (
        <RenderMap
            candidate={candidate}
            coordinates={coordinates}
        />
    );
};