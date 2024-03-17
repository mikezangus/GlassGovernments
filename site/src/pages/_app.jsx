import React from "react";
import "leaflet/dist/leaflet.css";
import Header from "../components/Header";
import "../styles/index.css";


export default function App({ Component, pageProps }) {
    return (
        <>
        <Header />
        <main>
            <Component {...pageProps} />
        </main>
        </>
    );
};
