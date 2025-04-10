import React from "react";
import { Analytics } from "@vercel/analytics/react";
import { SpeedInsights } from "@vercel/speed-insights/next"; 
import Header from "../components/Header";
import "leaflet/dist/leaflet.css";
import "../styles/index.css";


export default function App({ Component, pageProps }) {
    return (
        <>
            <Analytics />
            <SpeedInsights />
            <Header />
            <main>
                <Component {...pageProps} />
            </main>
        </>
    );
};
