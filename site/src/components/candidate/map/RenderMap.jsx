import React from "react";
import { MapContainer, TileLayer } from "react-leaflet";
import CreateHeatmap from "./CreateHeatmap";
import "../../../css/candidate.css";


export default function RenderMap({ candID, coords }) {

    const position = [39.8282, -98.5696];
    
    return (

        <div className="map">

            <MapContainer
                key={`${candID}`}
                center={position}
                zoom={4}
                maxZoom ={10}
                style={{ height: "450px", width: "100%" }}
            >

                <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

                <CreateHeatmap coords={coords}/>

            </MapContainer>

        </div>

    );

};