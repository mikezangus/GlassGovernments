import React, { useState, useEffect } from "react";
import "../css/switch.css";

export default function SelectChamber({ onChamberSelect }) {

    const [chambers, setChambers] = useState([]);

    const fetchChambers = async () => {
        try {
            const response = await fetch("http://localhost:4000/api/chambers");
            if (!response.ok) throw new Error("Network response for chambers endpoint was not ok");
            const data = await response.json();
            setChambers(data);
            setSelectedChamber(data[0]?._id);
        } catch (error) {
            console.error("Error fetching chambers data ", error)
        }
    };

    useEffect(() => {
        fetchChambers();
    }, []);

    return (
        <div className="switch">
            {chambers.map((chamber) => (
                <button
                    key={chamber._id}
                    className="slider-button"
                    onClick={() => onChamberSelect(chamber._id)}
                >
                    {chamber._id}
                </button>
            ))}
        </div>
    );
};