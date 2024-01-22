import React from "react";
import "../../css/dropdown.css";
import formatContributionAmount from "./utilities/formatContributionAmount";


export default function RenderCandidates({ candidates, selectedCandidate, isOpen, toggleDropdown, handleCandidateClick }) {
    return (
        <div className="dropdown">
            <button className="dropdown__button" onClick={toggleDropdown}>
                {selectedCandidate ? `${selectedCandidate._id.firstName} ${selectedCandidate._id.lastName}` : "Click to select a candidate"}
            </button>
            {isOpen && (
                <div className="dropdown__menu" style={{ display: "block" }}>
                    {candidates.map((candidate) => {
                        const { _id: { firstName, lastName, party }, totalContributionAmount } = candidate;
                        const partyFormatted = party ? `(${party.charAt(0)})` : "";
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