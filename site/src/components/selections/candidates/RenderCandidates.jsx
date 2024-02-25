import React from "react";
import capitalizeWord from "../../utilities/capitalizeWord";
import formatContributionAmount from "../../utilities/formatContributionPreview";
import styles from "../../../styles/Dropdown.module.css"


export default function RenderCandidates({ candidates, selectedCandidate, isOpen, toggleDropdown, handleCandidateClick }) {
    // const minContributionAmount = 1000;
    return (
        <div className={styles.dropdown}>
            <div className={styles.container}>
                <button
                    className={
                        `${styles.button}
                        ${isOpen
                            ? styles.active
                            : ""
                        }`
                    }
                    onClick={toggleDropdown}
                >
                    {
                        selectedCandidate
                            ? `Candidate: ${capitalizeWord(selectedCandidate.name)}`
                            : "Select a candidate ▽"
                    }
                </button>
                {isOpen && (
                    <div className={styles.menu}>
                        {candidates
                            // .filter(candidate => candidate.totalContributionAmount > minContributionAmount)
                            .map((candidate) => {
                                const { totalContAmt, candID, name, party } = candidate;
                                const partyFormatted = party
                                    ? `(${party.charAt(0)})`
                                    : "";
                                return (
                                    <button
                                        className={styles.item}
                                        key={`${candID}`}
                                        onClick={() => handleCandidateClick(candidate)}
                                    >
                                        {capitalizeWord(name)} {partyFormatted} - ${formatContributionAmount(totalContAmt)}
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
