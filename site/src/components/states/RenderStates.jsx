import React from "react";
import "../../css/dropdown.css";


export default function RenderStates({ states, selectedState, isOpen, toggleDropdown, handleStateClick }) {
    return (
        <div className="dropdown">
            <button className="dropdown__button" onClick={toggleDropdown}>
                {selectedState ? `State selected: ${selectedState}` : "Click to select a state"}
            </button>
            {isOpen && (
                <div className="dropdown__menu" style={{ display: "block" }}>
                    {states.map((state) => (
                        <button
                            className="dropdown__item"
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