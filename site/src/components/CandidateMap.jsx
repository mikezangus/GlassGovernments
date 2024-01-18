import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, useMap } from "react-leaflet";
import "leaflet.heat";
import L from "leaflet";
import "leaflet.heat";


function HeatMapLayer({ data }) {

    const map = useMap();

    useEffect(() => {
        if (data && data.length > 0) {
            const heatData = data.map(item => [
                item.lat,
                item.lon,
                item.amount
            ]);
            const heatLayer = L.heatLayer(
                heatData, { radius: 25 }
            ).addTo(map);
            return () => {
                map.removeLayer(heatLayer);
            };
        }
    }, [data, map]);

    return null;

};


export default function DisplayCandidateMap({ chamber, state, district, candidate }) {

    const { _id: { firstName, lastName, party } } = candidate;
    const [data, setData] = useState([]);

    const fetchData = async () => {
        try {
            const params = new URLSearchParams({
                chamber: chamber,
                state: state,
                district: district,
                firstName: firstName,
                lastName: lastName,
                party: party
            });
            const url = `http://localhost:4000/api/candidatemap?${params.toString()}`;
            const response = await fetch(url);
            if (!response.ok) throw new Error("Network response for display candidate map was not ok");
            const data = await response.json();
            setData(data);
        } catch (error) {
            console.error("Error fetching candidate data: ", error);
            setData([]);
        };
    };

    useEffect(() => {
        if (chamber && state && district && candidate) {
            fetchData();
        }
    }, [chamber, state, district, candidate]);

    const coordinateCenter = [44.58, 104.46];
    const zoom = 13;

    return (
        <div>
            <MapContainer
                center={coordinateCenter}
                zoom={zoom}
                style={{ height: "100vh", width: "100%" }}
            >
                <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution="&copy; <a href'https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors"
                />
                <HeatMapLayer data={data} />
            </MapContainer>
        </div>
    );
};