import React from "react";
import showStateName from "../../utilities/showStateName";
import styles from "../../../styles/Dropdown.module.css";


export default function RenderStates({ states, selectedState, isOpen, toggleDropdown, handleStateClick }) {
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
