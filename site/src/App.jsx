import React, { useState } from "react";
import ShowChambers from "./components/chambers/ShowChambers";
import ShowStates from "./components/states/ShowStates";
import ShowDistricts from "./components/districts/ShowDistricts";
import useCountDistricts from "./components/districts/useCountDistricts";
import ShowCandidates from "./components/candidates/ShowCandidates";
import RenderCandidate from "./components/candidate/RenderCandidate";

import "./css/index.css"


export default function App() {

    const [selectedChamber, setSelectedChamber] = useState(null);
    const [selectedState, setSelectedState] = useState(null);
    const [selectedDistrict, setSelectedDistrict] = useState(null);
    const [selectedCandidate, setSelectedCandidate] = useState(null);

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
    };

    return (

        <main>

            <div className="leff">

                <ShowChambers
                    onChamberSelect={handleChamberSelection}
                />

                {selectedChamber && (
                    <ShowStates
                        chamber={selectedChamber}
                        onStateSelect={handleStateSelection}
                    />
                )}

                {selectedChamber === "HOUSE" && selectedState && districtCount > 1 && (
                    <ShowDistricts
                        chamber={selectedChamber}
                        state={selectedState}
                        onDistrictSelect={handleDistrictSelection}
                    />
                )}

                {selectedChamber && selectedState && selectedDistrict && (
                    <ShowCandidates
                        chamber={selectedChamber}
                        state={selectedState}
                        district={selectedDistrict}
                        onCandidateSelect={handleCandidateSelection}
                    />
                )}

            </div>

            <div className="right">

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