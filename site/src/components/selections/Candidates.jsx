import { useState } from "react";
import useFetchCandidates from "../../hooks/useFetchCandidates";
import capitalizeWord from "../../lib/capitalizeWord";
import formatContAmt from "../../lib/formatContAmt";
import styles from "../../styles/selections/Dropdown.module.css";


function Renderer({ candidates, selectedCandidate, isOpen, toggleDropdown, handleCandidateClick }) {
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
                            ? `Candidate: ${selectedCandidate.name}`
                            : "Select a candidate ▽"
                    }
                </button>
                {isOpen && (
                    <div className={styles.menu}>
                        {candidates
                            .filter(candidate => candidate.amt > 1000)
                            .sort((a, b) => b.amt - a.amt)
                            .map((candidate) => {
                                const { amt, candId, name, party } = candidate;
                                const partyFormatted = party
                                    ? `(${party.charAt(0)})`
                                    : "";
                                return (
                                    <button
                                        className={styles.item}
                                        key={`${candId}`}
                                        onClick={() => handleCandidateClick(candidate)}
                                    >
                                        {capitalizeWord(name)} {partyFormatted} - ${formatContAmt(amt)}
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
