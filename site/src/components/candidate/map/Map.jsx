import { useState } from "react";
import dynamic from "next/dynamic";
import useFetchCoords from "./useFetchCoords";


export default function Map({ year, candidate }) {
    const [coords, setCoords] = useState([]);
    const { candID } = candidate;
    useFetchCoords(year, candID, setCoords);
    const DynamicRenderMap = dynamic(
        () => import("./RenderMap"),
        { ssr: false }
    );
    return (
        <DynamicRenderMap
            candID={candID}
            coords={coords}
        />
    );
};
