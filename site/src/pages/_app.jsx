import React, { useEffect } from "react";
import Header from "../components/Header";
import "../styles/index.css";
import "leaflet/dist/leaflet.css";



export default function App({ Component, pageProps }) {

    const createIndexes = async() => {
        const response = await fetch(
            "/api/createIndexes",
            { method: "POST" }
        );
    };

    useEffect(() => createIndexes(), []);

    return (
        <>
        <Header />
        <main>
            <Component {...pageProps} />
        </main>
        </>
    );
};
