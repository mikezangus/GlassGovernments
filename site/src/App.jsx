import React, { useState } from "react";
import RenderHeader from "./components/header/Header";
import RenderSelections from "./components/selections/RenderSelections";
import RenderCandidate from "./components/candidate/RenderCandidate";
import "./css/index.css"


export default function App() {

    const [selectedYear, setSelectedYear] = useState(null);
    const [selectedChamber, setSelectedChamber] = useState(null);
    const [selectedState, setSelectedState] = useState(null);
    const [selectedDistrict, setSelectedDistrict] = useState(null);
    const [selectedCandidate, setSelectedCandidate] = useState(null);

    const handleYearSelection = (year) => {
        setSelectedYear(year);
        setSelectedChamber(null);
    }
    const handleChamberSelection = (chamber) => {
        setSelectedChamber(chamber);
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

        <body>

            <RenderHeader />

            <main>

                <RenderSelections
                    handleYearSelection={handleYearSelection}
                    selectedYear={selectedYear}
                    handleChamberSelection={handleChamberSelection}
                    selectedChamber={selectedChamber}
                    handleStateSelection={handleStateSelection}
                    selectedState={selectedState}
                    handleDistrictSelection={handleDistrictSelection}
                    selectedDistrict={selectedDistrict}
                    handleCandidateSelection={handleCandidateSelection}
                />


                {selectedYear && selectedChamber && selectedState && selectedDistrict && selectedCandidate && (
                    <RenderCandidate
                        year={selectedYear}
                        chamber={selectedChamber}
                        state={selectedState}
                        district={selectedDistrict}
                        candidate={selectedCandidate}
                    />
                )}

            </main>

        </body>

    );
};