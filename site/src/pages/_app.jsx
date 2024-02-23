import React, { useEffect } from "react";
import Header from "../components/header/Header";
import "../styles/index.css";
import "leaflet/dist/leaflet.css";



export default function App({ Component, pageProps }) {

    const createIndexes = async() => {
        const response = await fetch(
            "/api/createIndexes",
            { method: "POST" }
        );
        if (response.ok) {
            console.log("indexes created");
        } else {
            console.log("failed to create indexes");
        }
    }

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
