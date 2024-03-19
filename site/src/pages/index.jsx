import React, { useState } from "react";
import Head from "next/head";
import HTMLHead from "../components/HTMLHead";
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
            <HTMLHead />
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
