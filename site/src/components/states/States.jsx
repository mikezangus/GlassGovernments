import { useState } from "react";
import useFetchStates from "./StatesFetcher";
import StatesDropdown from "./StateSelector";


export default function SelectState({ chamber, onStateSelect }) {

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

    return StatesDropdown(states, selectedState, isOpen, toggleDropdown, handleStateClick);
    
};