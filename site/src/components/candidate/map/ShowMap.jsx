import { useState } from "react";
import useFetchCoords from "./useFetchCoords";
import RenderMap from "./RenderMap";


export default function ShowMap({ year, candidate }) {
    const [coords, setCoords] = useState([]);
    const { candID } = candidate;
    useFetchCoords(year, candID, setCoords);
    console.log("COORDS from component", coords)
    return (
        <RenderMap
            candID={candID}
            coords={coords}
        />
    );
};