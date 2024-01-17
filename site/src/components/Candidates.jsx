import React, { useState, useEffect } from "react";
import "../css/dropdown.css";


function formatContributionAmount(amount) {
    return (
        amount >= 10000000 ? `${(amount / 1000000).toFixed(1)}M` : // $60,900,000 => $60.9M
        amount >= 1000000 ? `${(amount / 1000000).toFixed(2)}M` : // $6,090,000 => $6.09M
        amount >= 100000 ? `${(amount / 1000).toFixed(0)}K` : // $609,000 => $609K
        amount >= 10000 ? `${(amount / 1000).toFixed(1)}K` : // $60,900 => $60.9K
        amount >= 1000 ? `${(amount / 1000).toFixed(2)}K` : // $6,090 => $6.09K
        `${amount}` // $609 => $609
    );
};


function sortCandidates(candidates) {
    return candidates.sort((a, b) => b.totalContributionAmount - a.totalContributionAmount);
};


export default function SelectCandidate({ chamber, state, district, onCandidateSelect }) {

    const [candidates, setCandidates] = useState([]);
    const [selectedCandidate, setSelectedCandidate] = useState(null);
    const [isOpen, setIsOpen] = useState(false);

    const fetchCandidates = async () => {
        try {
            const params = new URLSearchParams({
                chamber: chamber,
                state: state,
                district: district
            });
            const url = `http://localhost:4000/api/candidates?${params.toString()}`;
            const response = await fetch(url); 
            if(!response.ok) throw new Error("Network response for candidates endpoint was not ok");
            const data = await response.json();
            const sortedData = sortCandidates(data);
            setCandidates(sortedData);
        } catch (error) {
            console.error("Error fetching candidates data: ", error)
        }
    };

    useEffect(() => {
        if (chamber && state && district) {
            fetchCandidates();
        }
    }, [chamber, state, district]);

    const handleCandidateClick = (candidate) => {
        onCandidateSelect(candidate);
        setSelectedCandidate(candidate._id)
        setIsOpen(false);
    };

    const toggleDropdown = () => setIsOpen(!isOpen);

    return (
        <div className="dropdown">
            <button className="dropdown__button" onClick={toggleDropdown}>
                {selectedCandidate ? `Candidate selected: ${selectedCandidate.lastName}` : "Click to select a candidate"}
            </button>
            {isOpen && (
                <div className="dropdown__menu" style={{ display: "block" }}>
                    {candidates.map((candidate) => {
                        const { firstName, lastName, party } = candidate._id;
                        const partyFormatted = party ? `(${party.charAt(0)})` : `("")`;
                        const { totalContributionAmount } = candidate;
                        return (
                            <button
                                className="dropdown__item"
                                key={`${firstName}-${lastName}-${party}`}
                                onClick={() => handleCandidateClick(candidate)}
                            >
                                {firstName} {lastName} {partyFormatted} - ${formatContributionAmount(totalContributionAmount)}
                            </button>
                        )
                        })}
                </div>
            )}
        </div>
    );
};