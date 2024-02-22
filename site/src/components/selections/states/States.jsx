import { useState } from "react";
import useFetchStates from "./useFetchStates";
import RenderStates from "./RenderStates";


export default function States({ year, office, selectedState, onStateSelect }) {

    const [states, setStates] = useState([]);
    const [isOpen, setIsOpen] = useState(false);

    useFetchStates(year, office, setStates);

    const toggleDropdown = () => setIsOpen(!isOpen);
    const handleStateClick = (state) => {
        onStateSelect(state);
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
