import { useState } from "react";
import useFetchCandidates from "../../hooks/useFetchCandidates";
import capitalizeWord from "../../lib/capitalizeWord";
import formatContAmt from "../../lib/formatContAmt";
import styles from "../../styles/selections/Dropdown.module.css";


function Renderer({ candidates, selectedCandidate, isOpen, toggleDropdown, handleCandidateClick }) {
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
                                        {capitalizeWord(name)} {partyFormatted} - ${formatContAmt(totalContAmt)}
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


export default function Candidates({ year, office, state, district, onCandidateSelect }) {

    const [candidates, setCandidates] = useState([]);
    const [selectedCandidate, setSelectedCandidate] = useState(null);
    const [isOpen, setIsOpen] = useState(false);

    useFetchCandidates(year, office, state, district, setCandidates);

    const toggleDropdown = () => setIsOpen(!isOpen);
    const handleCandidateClick = (candidate) => {
        onCandidateSelect(candidate);
        setSelectedCandidate(candidate);
        setIsOpen(false);
    };

    return (
        <Renderer
            candidates={candidates}
            selectedCandidate={selectedCandidate}
            isOpen={isOpen}
            toggleDropdown={toggleDropdown}
            handleCandidateClick={handleCandidateClick}
        />
    );
    
};
