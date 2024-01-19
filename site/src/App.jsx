import React, { useState, useEffect } from "react";
import SelectChamber from "./components/Chambers";
import SelectState from "./components/States";
import SelectDistrict from "./components/Districts";
import SelectCandidate from "./components/Candidates";
import DisplayCandidateInfo from "./components/CandidateInfo";
import DisplayCandidateMap from "./components/CandidateMap";


export default function App() {

    const [selectedChamber, setSelectedChamber] = useState(null);
    const [selectedState, setSelectedState] = useState(null);
    const [districtCount, setDistrictCount] = useState(0);
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
            const params = new URLSearchParams({ chamber, state });
            const url = `http://localhost:4000/api/districts?${params.toString()}`;
            const response = await fetch(url);
            if (!response.ok) throw new Error("Network response for districts endpoint was not ok");
            const data = await response.json();
            if (data.length === 1) { handleDistrictSelection(data[0]) };
            setDistrictCount(data.length);
        } catch (error) {
            console.error("Error calculating district amount ", error);
            setDistrictCount(0);
        };
    };
    useEffect(() => {
        if (selectedChamber === "HOUSE" && selectedState) {
            calculateDistrictCount(selectedChamber, selectedState);
        }
    }, [selectedChamber, selectedState])

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
                    <DisplayCandidateInfo
                        chamber={selectedChamber}
                        state={selectedState}
                        district={selectedDistrict}
                        candidate={selectedCandidate}
                        onCandidateDisplay={handleCandidateDisplay}
                    />
                )}

                {selectedChamber && selectedState && selectedDistrict && selectedCandidate && (
                    <DisplayCandidateMap
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