import React from "react";
import showStateName from "../../utilities/showStateName";
import "../../../css/dropdown.css";


export default function RenderStates({ states, selectedState, isOpen, toggleDropdown, handleStateClick }) {
    return (
        <div className="dropdown">
            <div className="container">
                <button
                        className={`button ${isOpen ? "active" : ""}`}
                        onClick={toggleDropdown}
                    >
                        {
                            selectedState
                                ? `State: ${showStateName(selectedState)}`
                                : "Select a state ▽"
                        }
                    </button>
                    {isOpen && (
                        <div className="menu">
                            {states.map((state) => (
                                <button
                                    className="item"
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