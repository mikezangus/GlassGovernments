import { useEffect } from "react";
import { useMap } from "react-leaflet";
import "leaflet.heat";
import L from "leaflet";


export default function CreateHeatmapLayer({ coordinates }) {
    const map = useMap();
    useEffect(() => {
        if (!map || !coordinates || coordinates.length === 0) return;
        const points = coordinates.map(coord => [
            coord.lat, coord.lng, coord.amount
        ]);
        const heatmapLayer = L.heatLayer(points, {
            radius: 20, blur: 15, maxZoom: 17
        });
        heatmapLayer.addTo(map);
        return () => {map.removeLayer(heatmapLayer)};
    }, [map, coordinates]);
    return null;
};