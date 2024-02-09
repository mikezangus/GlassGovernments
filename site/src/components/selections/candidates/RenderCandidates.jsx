import React from "react";
import "../../../css/dropdown.css";
import capitalizeWord from "../../utilities/capitalizeWord";
import formatContributionAmount from "../../utilities/formatContributionPreview";


export default function RenderCandidates({ candidates, selectedCandidate, isOpen, toggleDropdown, handleCandidateClick }) {
    const minContributionAmount = 1000;
    return (
        <div className="dropdown">
            <div className="container">
                <button
                    className={`button ${isOpen ? "active" : ""}`}
                    onClick={toggleDropdown}
                >
                    {
                        selectedCandidate
                            ? `Candidate: ${capitalizeWord(selectedCandidate.name)}`
                            : "Select a candidate ▽"
                    }
                </button>
                {isOpen && (
                    <div className="menu">
                        {candidates
                            .filter(candidate => candidate.totalContributionAmount > minContributionAmount)
                            .map((candidate) => {
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
                                        {capitalizeWord(name)} {partyFormatted} - ${formatContributionAmount(totalContributionAmount)}
                                    </button>
                                )
                            })
                        }
                    </div>
                )}
            </div>

        </div>
    );
};