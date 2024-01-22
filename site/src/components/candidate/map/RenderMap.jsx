import React from "react";
import { MapContainer, TileLayer } from "react-leaflet";
import CreateHeatmapLayer from "./CreateHeatmapLayer";


export default function RenderMap({ candidate, coordinates }) {
    const { _id: { firstName, lastName, party } } = candidate;
    const position = [39.8282, -98.5696];
    return (
        <MapContainer
            key={`${firstName}-${lastName}-${party}`}
            center={position}
            zoom={4}
            maxZoom ={10}
            style={{ height: "500px", width: "100% " }}
        >
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            <CreateHeatmapLayer coordinates={coordinates}/>
        </MapContainer>
    );
};