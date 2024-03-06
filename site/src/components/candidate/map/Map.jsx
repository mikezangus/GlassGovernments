import { useState } from "react";
import dynamic from "next/dynamic";
import useFetchCoords from "../../../hooks/useFetchCoords";


export default function Map({ year, state, candidate }) {
    const [coords, setCoords] = useState([]);
    const { candID } = candidate;
    useFetchCoords(year, candID, setCoords);
    const DynamicRenderMap = dynamic(
        () => import("./RenderMap"),
        { ssr: false }
    );
    return (
        <DynamicRenderMap
            state={state}
            candID={candID}
            coords={coords}
        />
    );
};
