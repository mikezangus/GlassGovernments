import React, { useState } from "react";
import SelectChamber from "./components/Chambers";
import SelectState from "./components/States";
import SelectDistrict from "./components/Districts";
import SelectCandidate from "./components/Candidates";


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
        setSelectedCandidate(null)
    };
    const handleCandidateSelection = (candidate) => {
        setSelectedCandidate(candidate);
    }

    return (
        <main>

            <SelectChamber
                onChamberSelect={handleChamberSelection}
            />

            {selectedChamber && (
                <SelectState
                    selectedChamber={selectedChamber}
                    onStateSelect={handleStateSelection}

                />
            )}

            {selectedChamber && selectedState && (
                <SelectDistrict
                    selectedChamber={selectedChamber}
                    selectedState={selectedState}
                    onDistrictSelect={handleDistrictSelection}
                />
            )}

            {selectedChamber && selectedState && selectedDistrict && (
                <SelectCandidate
                    selectedChamber={selectedChamber}
                    selectedState={selectedState}
                    selectedDistrict={selectedDistrict}
                    onCandidateSelect={handleCandidateSelection}
                />
            )}

        </main>
    );
};