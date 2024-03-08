import { useState } from "react";
import useFetchStates from "../../hooks/useFetchStates";
import showStateName from "../../lib/showStateName";
import styles from "../../styles/selections/Dropdown.module.css";


function RenderButton({ isOpen, toggleDropdown, selectedState }) {
    return (
        <button
            className={`
                ${styles.button}
                ${isOpen ? styles.active : ""}
            `}
            onClick={toggleDropdown}
        >
            {
                selectedState
                    ? `State: ${showStateName(selectedState)}`
                    : "Select a state"
            }
        </button>
    );
};


function RenderMenu({ states, handleStateClick }) {
    return (
        <div className={styles.menu}>
            {states.map((state) => (
                <button
                    className={styles.item}
                    key={state}
                    onClick={() => handleStateClick(state)}
                >
                    {showStateName(state)}
                </button>
            ))}
        </div>
    );
};


function Renderer({ isOpen, toggleDropdown, selectedState, states, handleStateClick }) {
    return (
        <div className={styles.container}>
            <RenderButton
                isOpen={isOpen}
                toggleDropdown={toggleDropdown}
                selectedState={selectedState}
            />
            {isOpen && (
                <RenderMenu
                    states={states}
                    handleStateClick={handleStateClick}
                />
            )}
        </div>
    );
};


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
        <Renderer
            states={states}
            selectedState={selectedState}
            isOpen={isOpen}
            toggleDropdown={toggleDropdown}
            handleStateClick={handleStateClick}
        />
    );
    
};
