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
                        ? `Candidate: ${selectedCandidate._id.firstName} ${selectedCandidate._id.lastName}`
                        : "Select a candidate ▽"
                }
            </button>
            {isOpen && (
                <div className="menu">
                    {candidates.map((candidate) => {
                        const { _id: { firstName, lastName, party }, totalContributionAmount } = candidate;
                        const partyFormatted = party
                            ? `(${party.charAt(0)})`
                            : "";
                        return (
                            <button
                                className="item"
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