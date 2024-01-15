import React, { useState, useEffect } from "react";
import "../css/dropdown.css";


export default function SelectState({ chamber, onStateSelect }) {

    const state = null;
    const [states, setStates] = useState([]);
    const [isOpen, setIsOpen] = useState(false);

    const fetchStates = async () => {
        try {
            const response = await fetch(`http://localhost:4000/api/states?chamber=${encodeURIComponent(chamber)}`);
            if (!response.ok) throw new Error("Network response for states endpoint was not ok");
            const data = await response.json();
            setStates(data);
        } catch (error) {
            console.error("Error fetching states data ", error)
        }
    };

    useEffect(() => {
        if (chamber) {
            fetchStates();
        }
    }, [chamber]);

    const handleStateClick = (state) => {
        onStateSelect(state);
        setIsOpen(false);
    };

    const toggleDropdown = () => setIsOpen(!isOpen);

    return (
        <div className="dropdown">
            <button className="dropdown__button" onClick={toggleDropdown}>
                {state ? `State selected: ${state}` : "Click to select a state"}
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