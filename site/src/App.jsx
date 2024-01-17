import React, { useState } from "react";
import SelectChamber from "./components/Chambers";
import SelectState from "./components/States";
import SelectDistrict from "./components/Districts";
import SelectCandidate from "./components/Candidates";
import DisplayCandidate from "./components/Candidate";


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
        calculateDistrictCount(selectedChamber, state)
    };

    const handleDistrictSelection = (district) => {
        setSelectedDistrict(district);
        setSelectedCandidate(null);
    };
    const handleCandidateSelection = (candidate) => {
        setSelectedCandidate(candidate);
        setDisplayedCandidate(null);
    };
    const handleCandidateDisplay = (candidate) => {
        setDisplayedCandidate(candidate)
    };
    const calculateDistrictCount = async (chamber, state) => {
        try {
            const params = new URLSearchParams({
                chamber: chamber,
                state: state
            });
            const url = `http://localhost:4000/api/districts?${params.toString()}`;
            const response = await fetch(url);
            if (!response.ok) throw new Error("Network response for districts endpoint was not ok");
            const data = await response.json();
            if (data.length === 1) {
                handleDistrictSelection(data[0]);
            }
        } catch (error) {
            console.error("Error calculating district amount ", error);
        };
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

                {selectedChamber && selectedState && selectedDistrict === null && (
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
                    <DisplayCandidate
                        chamber={selectedChamber}
                        state={selectedState}
                        district={selectedDistrict}
                        candidate={selectedCandidate}
                        onCandidateDisplay={handleCandidateDisplay}
                    />
                )}

            </div>

        </main>

    );
};