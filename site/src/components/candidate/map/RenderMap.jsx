import React from "react";
import { MapContainer, TileLayer } from "react-leaflet";
import CreateHeatmap from "./CreateHeatmap";
import styles from "../../../styles/Candidate.module.css";


export default function RenderMap({ state, candID, coords }) {
    let position = []
    let zoom
    state === "AK" || state === "HI"
        ? (
            position = [50, -115],
            zoom = 2
        )
        : (
            position = [38, -98],
            zoom = 4
        );
    
    return (

        <div className={styles.map}>

            <MapContainer
                key={`${candID}`}
                center={position}
                zoom={zoom}
                maxZoom ={12}
                style={{ height: "100%", width: "100%" }}
            >

                <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

                <CreateHeatmap coords={coords}/>

            </MapContainer>

        </div>

    );

};
