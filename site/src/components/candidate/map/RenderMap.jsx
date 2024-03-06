import React, {useEffect, useState } from "react";
import { MapContainer, TileLayer } from "react-leaflet";
import CreateHeatmap from "./CreateHeatmap";
import styles from "../../../styles/candidate/Map.module.css";


export default function RenderMap({ state, candId, coords }) {

    const [isMobile, setIsMobile] = useState(window.innerWidth < 768);
    useEffect(() => {
        const handleResize = () => {
            setIsMobile(window.innerWidth < 768);
        };
        window.addEventListener("resize", handleResize);
        return () => 
            window.removeEventListener("resize", handleResize);
    }, []);

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
            >

                <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

                <CreateHeatmap coords={coords}/>

            </MapContainer>

        </div>

    );

};
