import React, { useState } from "react";
import Head from "next/head";
import Selections from "../components/Selections";
import Candidate from "../components/Candidate";


export default function Home() {

    const [selectedYear, setSelectedYear] = useState(null);
    const [selectedOffice, setSelectedOffice] = useState(null);
    const [selectedState, setSelectedState] = useState(null);
    const [selectedDistrict, setSelectedDistrict] = useState(null);
    const [selectedCandidate, setSelectedCandidate] = useState(null);

    const handleYearSelection = (year) => {
        setSelectedYear(year);
        setSelectedOffice(null);
    }
    const handleOfficeSelection = (chamber) => {
        setSelectedOffice(chamber);
        setSelectedState(null);
    };
    const handleStateSelection = (state) => {
        setSelectedState(state);
        setSelectedDistrict(null);
    };
    const handleDistrictSelection = (district) => {
        setSelectedDistrict(district);
        setSelectedCandidate(null);
    };
    const handleCandidateSelection = (candidate) => {
        setSelectedCandidate(candidate);
    };

    return (

        <>
        <Head>
            <meta charset="utf-8" />
            <meta
                name="viewport"
                content="width=device-width, initial-scale=1"
            />
            <title>
                Glass Governments
            </title>
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
                content="https://glassgovernments.com"
            />
            <meta
                property="og:title"
                content="Glass Governments"
            />
            <meta
                property="og:description"
                content=""
            />
            <meta
                property="og:image"
                content="https://glass-governments.vercel.app/og_image.png"
            />
        </Head>

        <Selections
            handleYearSelection={handleYearSelection}
            selectedYear={selectedYear}
            handleOfficeSelection={handleOfficeSelection}
            selectedOffice={selectedOffice}
            handleStateSelection={handleStateSelection}
            selectedState={selectedState}
            handleDistrictSelection={handleDistrictSelection}
            selectedDistrict={selectedDistrict}
            handleCandidateSelection={handleCandidateSelection}
            selectedCandidate={selectedCandidate}
        />

        {selectedYear && selectedOffice && selectedState && selectedDistrict && selectedCandidate && (
            <Candidate
                year={selectedYear}
                office={selectedOffice}
                state={selectedState}
                district={selectedDistrict}
                candidate={selectedCandidate}
            />
        )}

        </>

    );

};
