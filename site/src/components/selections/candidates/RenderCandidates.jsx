import React from "react";
import "../../../css/dropdown.css";
import formatContributionAmount from "../../utilities/formatContributionPreview";


export default function RenderCandidates({ candidates, selectedCandidate, isOpen, toggleDropdown, handleCandidateClick }) {
    return (
        <div className="dropdown">
             <button
                className={`button ${isOpen ? "active" : ""}`}
                onClick={toggleDropdown}
            >
                {
                    selectedCandidate
                        ? `Candidate: ${selectedCandidate.name}`
                        : "Select a candidate ▽"
                }
            </button>
            {isOpen && (
                <div className="menu">
                    {candidates.map((candidate) => {
                        const { totalContributionAmount, candID, name, party } = candidate;
                        const partyFormatted = party
                            ? `(${party.charAt(0)})`
                            : "";
                        return (
                            <button
                                className="item"
                                key={`${candID}`}
                                onClick={() => handleCandidateClick(candidate)}
                            >
                                {name} {partyFormatted} - ${formatContributionAmount(totalContributionAmount)}
                            </button>
                        )
                    })}
                </div>
            )}
        </div>
    );
};