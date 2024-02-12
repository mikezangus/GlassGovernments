import { useEffect } from "react";
import { useMap } from "react-leaflet";
import "leaflet.heat";
import L from "leaflet";


export default function CreateHeatmap({ coords }) {
    console.log("COORDS FROM MAP:", coords)
    const map = useMap();
    useEffect(() => {
        if (!map || !coords || coords.length === 0) return;
        const points = coords.map(({ coordinates }) => {
            const lat = coordinates[1];
            const lon = coordinates[0];
            return [lat, lon]
        });
        const heatmapLayer = L.heatLayer(points, {
            radius: 20, blur: 20, maxZoom: 17
        });
        heatmapLayer.addTo(map);
        return () => {map.removeLayer(heatmapLayer)};
    }, [map, coords]);
    return null;
};