import { useState } from "react";
import dynamic from "next/dynamic";
import useFetchCoords from "../../../hooks/useFetchCoords";


export default function Map({ year, state, candidate }) {
    const [coords, setCoords] = useState([]);
    const { candId } = candidate;
    useFetchCoords(year, candId, setCoords);
    const DynamicRenderMap = dynamic(
        () => import("./RenderMap"),
        { ssr: false }
    );
    return (
        <DynamicRenderMap
            state={state}
            candId={candId}
            coords={coords}
        />
    );
};
