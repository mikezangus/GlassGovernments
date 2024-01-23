import { useState } from "react";
import useFetchStates from "./useFetchStates";
import RenderStates from "./RenderStates";


export default function ShowStates({ chamber, onStateSelect }) {

    const [states, setStates] = useState([]);
    const [selectedState, setSelectedState] = useState(null);
    const [isOpen, setIsOpen] = useState(false);

    useFetchStates(chamber, setStates);

    const toggleDropdown = () => setIsOpen(!isOpen);
    const handleStateClick = (state) => {
        onStateSelect(state);
        setSelectedState(state);
        setIsOpen(false);
    };

    return (
        <RenderStates
            states={states}
            selectedState={selectedState}
            isOpen={isOpen}
            toggleDropdown={toggleDropdown}
            handleStateClick={handleStateClick}
        />
    );
    
};