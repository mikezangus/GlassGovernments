import React from "react";
import Head from "next/head";


export default function HTMLHead() {
    const url = "https://glassgovernments.com";
    const title = "Glass Governments";
    const description = "";
    const imageURL = "https://glass-governments.vercel.app/og_image.png";
    return( 
        <Head>
        <meta charset="utf-8" />
        <meta
            name="viewport"
            content="width=device-width, initial-scale=1"
        />
        <title>{title}</title>
        <link
            rel="stylesheet"
            href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"
        />
        <meta
            property="og:type"
            content="website"
        />
        <meta
            property="og:url"
            content={url}
        />
        <meta
            property="og:title"
            content={title}
        />
        <meta
            property="og:description"
            content={description}
        />
        <meta
            property="og:image"
            content={imageURL}
        />
        <meta
            property="twitter:card"
            content="summary_large_image"
        />
        <meta
            property="twitter:url"
            content={url}
        />
        <meta
            property="twitter:title"
            content={title}
        />
        <meta
            property="twitter:description"
            content={description}
        />
        <meta
            property="twitter:image"
            content={imageURL}
        />
        </Head>
    );
};
