import { useState } from "react";
import useFetchStates from "../../hooks/useFetchStates";
import showStateName from "../../lib/showStateName";
import styles from "../../styles/Dropdown.module.css";


function Renderer({ states, selectedState, isOpen, toggleDropdown, handleStateClick }) {
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
                            selectedState
                                ? `State: ${showStateName(selectedState)}`
                                : "Select a state ▽"
                        }
                    </button>
                    {isOpen && (
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
                    )}
            </div>
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
