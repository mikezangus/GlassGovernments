import React, { useState, useEffect } from "react";
import "../css/dropdown.css";


export default function SelectCandidate({ selectedChamber, selectedState, selectedDistrict, onCandidateSelect, selectedCandidate }) {

    const [candidates, setCandidates] = useState([]);
    const [isOpen, setIsOpen] = useState(false);

    const fetchCandidates = async () => {
        try {
            const districtURI = encodeURIComponent(selectedDistrict);
            const stateURI = encodeURIComponent(selectedState);
            const chamberURI = encodeURIComponent(selectedChamber)
            const response = await fetch(`http://localhost:4000/api/candidates?district=${districtURI}&state=${stateURI}&chamber=${chamberURI}`);
            if(!response.ok) throw new Error("Network response for candidates endpoint was not ok");
            const data = await response.json();
            setCandidates(data);
        } catch (error) {
            console.error("Error fetching candidates data: ", error)
        }
    };

    useEffect(() => {
        if (selectedChamber && selectedState && selectedDistrict) {
            fetchCandidates();
        }
    }, [selectedChamber, selectedState, selectedDistrict]);

    const handleCandidateClick = (candidate) => {
        onCandidateSelect(candidate);
        setIsOpen(false);
    };

    const toggleDropdown = () => setIsOpen(!isOpen);

    return (
        <div className="dropdown">
            <button className="dropdown__button" onClick={toggleDropdown}>
                {selectedCandidate ? `Candidate selected: ${selectedCandidate}` : "Click to select a candidate"}
            </button>
            {isOpen && (
                <div className="dropdown__menu" style={{ display: "block" }}>
                    {candidates.map((candidate) => {
                        const firstName = candidate.firstName
                        const lastName = candidate.lastName
                        const party = candidate.party
                        const partyFormatted = party ? `(${party.charAt(0)})` : `("")`;
                        return(
                            <button
                                className="dropdown__item"
                                key={`${firstName}-${lastName}-${party}`}
                                onClick={() => handleCandidateClick(candidate)}
                            >
                                {firstName} {lastName} {partyFormatted}
                            </button>
                        )
                        })}
                </div>
            )}
        </div>
    );
};