import { useState } from "react";
import useFetchCandidates from "./useFetchCandidates";
import RenderCandidates from "./RenderCandidates";


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
        <RenderCandidates
            candidates={candidates}
            selectedCandidate={selectedCandidate}
            isOpen={isOpen}
            toggleDropdown={toggleDropdown}
            handleCandidateClick={handleCandidateClick}
        />
    );
    
};