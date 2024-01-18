import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";


export default function DisplayCandidateMap({ chamber, state, district, candidate }) {

    const { _id: { firstName, lastName, party } } = candidate;
    const [coordinates, setCoordinates] = useState([]);

    const fetchCoordinateData = async () => {
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
            if (!response.ok) throw new Error("Network response for display candidate info was not ok")
            const data = await response.json();
            setCoordinates(data);
        } catch (error) {
            console.error("Error fetching candidate data: ", error);
            setCoordinates([]);
        };
    };

    useEffect(() => {
        if (chamber && state && district && candidate) {
            fetchCoordinateData();
        }
    }, [chamber, state, district, candidate]);

    const position = [39.8282, -98.5696];

    const dot = new L.DivIcon({
        className: "custom-dot-icon",
        html: '<div style="background-color: red; width: 10px; height: 10px; border-radius: 50%; position: relative; left: -5px; top: -5px;"></div>',
        iconSize: [10, 10]
    });

    return (

        <MapContainer
            center={position}
            zoom={4}
            style={{
                height: "500px",
                width: "100%"
            }}
        >

            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />

            {coordinates.map((coord, index) => {
                if (coord.lat != null & coord.lng != null) {
                    return (
                        <Marker
                            key={index}
                            position={[coord.lat, coord.lng]}
                            icon={dot}
                        >
                            <Popup>
                                Amount: ${coord.amount}
                            </Popup>
                        </Marker>
                    );
                }
                return null;
            })}

        </MapContainer>
    );
};