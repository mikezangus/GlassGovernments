import React from "react";
import { Analytics } from "@vercel/analytics/react"
import Header from "../components/Header";
import "leaflet/dist/leaflet.css";
import "../styles/index.css";


export default function App({ Component, pageProps }) {
    return (
        <>
            <Analytics />
            <Header />
            <main>
                <Component {...pageProps} />
            </main>
        </>
    );
};
