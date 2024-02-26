import { useEffect } from "react";
import { useMap } from "react-leaflet";
import "leaflet.heat";
import L from "leaflet";


export default function CreateHeatmap({ coords }) {
    console.log("CORDS FROM MAP:", coords)
    const map = useMap();
    const createHeatmap = ({ coords }) => {
        if (!map || !coords || coords.length === 0) return;
        const points = coords.map(({ COORDS, AMT }) => {
            if (COORDS && COORDS.coordinates) {
                const lat = COORDS.coordinates[1];
                const lon = COORDS.coordinates[0];
                return [lat, lon, AMT];
            }
            return null;
        }).filter(
            point => point !== null
        );
        const heatmapLayer = L.heatLayer(points, {
            radius: 7, blur: 9
        });
        heatmapLayer.addTo(map);
        return () => { map.removeLayer(heatmapLayer) };
    }
    useEffect(() =>
        createHeatmap({ coords }),
        [map, coords]
    );
    return null;
};
