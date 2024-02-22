import React from "react";
import Header from "../components/header/Header";
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
