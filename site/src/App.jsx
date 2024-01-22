import React, { useState } from "react";
import SelectChamber from "./components/chambers/Chambers";
import SelectState from "./components/states/States";
import SelectDistrict from "./components/districts/Districts";
import useCountDistricts from "./components/districts/DistrictCounter";
import SelectCandidate from "./components/candidates/Candidates";
import RenderCandidate from "./components/candidate/RenderCandidate";

import "./css/index.css"


export default function App() {

    const [selectedChamber, setSelectedChamber] = useState(null);
    const [selectedState, setSelectedState] = useState(null);
    const [selectedDistrict, setSelectedDistrict] = useState(null);
    const [selectedCandidate, setSelectedCandidate] = useState(null);
    const [displayedCandidate, setDisplayedCandidate] = useState(null);

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
    const districtCount = useCountDistricts(selectedChamber, selectedState, handleDistrictSelection);
    const handleCandidateSelection = (candidate) => {
        setSelectedCandidate(candidate);
        setDisplayedCandidate(null);
    };


    return (

        <main>

            <div className="left-half">

                <SelectChamber
                    onChamberSelect={handleChamberSelection}
                />

                {selectedChamber && (
                    <SelectState
                        chamber={selectedChamber}
                        onStateSelect={handleStateSelection}
                    />
                )}

                {selectedChamber === "HOUSE" && selectedState && districtCount > 1 && (
                    <SelectDistrict
                        chamber={selectedChamber}
                        state={selectedState}
                        onDistrictSelect={handleDistrictSelection}
                    />
                )}

                {selectedChamber && selectedState && selectedDistrict && (
                    <SelectCandidate
                        chamber={selectedChamber}
                        state={selectedState}
                        district={selectedDistrict}
                        onCandidateSelect={handleCandidateSelection}
                    />
                )}

            </div>

            <div className="right-half">

                {selectedChamber && selectedState && selectedDistrict && selectedCandidate && (
                   <RenderCandidate
                        chamber={selectedChamber}
                        state={selectedState}
                        district={selectedDistrict}
                        candidate={selectedCandidate}
                   />
                )}

            </div>

        </main>

    );
};