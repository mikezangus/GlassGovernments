import { useState } from "react";
import useFetchCandidates from "./CandidatesFetcher";
import CandidatesDropdown from "./CandidateSelector"


export default function SelectCandidate({ chamber, state, district, onCandidateSelect }) {

    const [candidates, setCandidates] = useState([]);
    const [selectedCandidate, setSelectedCandidate] = useState(null);
    const [isOpen, setIsOpen] = useState(false);

    useFetchCandidates(chamber, state, district, setCandidates);

    const toggleDropdown = () => setIsOpen(!isOpen);
    const handleCandidateClick = (candidate) => {
        onCandidateSelect(candidate);
        setSelectedCandidate(candidate);
        setIsOpen(false);
    };

    return CandidatesDropdown(candidates, selectedCandidate, isOpen, toggleDropdown, handleCandidateClick);
    
};