import React from "react";
import "../../../css/dropdown.css";


export default function RenderStates({ states, selectedState, isOpen, toggleDropdown, handleStateClick }) {
    return (
        <div className="dropdown">
            <button className="button" onClick={toggleDropdown}>
                {
                    selectedState
                        ? `State: ${selectedState}`
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
                            {state}
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
};