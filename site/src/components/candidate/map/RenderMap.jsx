import React, {useEffect, useState } from "react";
import { MapContainer, TileLayer } from "react-leaflet";
import CreateHeatmap from "./CreateHeatmap";
import useIsMobile from "../../../lib/useIsMobile";
import styles from "../../../styles/candidate/Map.module.css";


export default function RenderMap({ state, candId, coords }) {

    const isMobile = useIsMobile();

    let position = []
    let zoom
    state === "AK" || state === "HI"
        ? (
            position = [50, -115],
            zoom = 2
        )
        : (
            position = [38, -98],
            isMobile 
                ? zoom = 3
                : zoom = 4
        );
        
    return (

        <div className={styles.map}>

            <MapContainer
                key={`${candId}`}
                center={position}
                zoom={zoom}
                maxZoom ={12}
                style={{ height: "100%", width: "100%" }}
                attributionControl={false}
            >

                <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/>

                <CreateHeatmap coords={coords}/>

            </MapContainer>

        </div>

    );

};
