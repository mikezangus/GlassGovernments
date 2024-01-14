import React, { useState, useEffect } from "react";
import "../css/switch.css";

export default function SelectChamber({ onChamberSelect }) {

    const [chambers, setChambers] = useState([]);
    const [defaultSelectedChamber, setDefaultSelectedChamber] = useState(null);

    const fetchChambers = async () => {
        try {
            const response = await fetch("http://localhost:4000/api/chambers");
            if (!response.ok) throw new Error("Network response for chambers endpoint was not ok");
            const data = await response.json();
            setChambers(data);
            if (data.length > 0) {
                const firstChamber = data[0]._id;
                setDefaultSelectedChamber(firstChamber);
                onChamberSelect(firstChamber);
            }
        } catch (error) {
            console.error("Error fetching chambers data ", error)
        }
    };

    useEffect(() => {
        fetchChambers();
    }, []);

    const handleChamberClick = (chamberId) => {
        setDefaultSelectedChamber(chamberId);
        onChamberSelect(chamberId);
    };

    return (
        <div className="switch-container">
            {chambers.map((chamber) => (
                <button
                    key={chamber._id}
                    className={`switch-button ${defaultSelectedChamber === chamber._id ? "active" : ""}`}
                    onClick={() => handleChamberClick(chamber._id)}
                >
                    {chamber._id}
                </button>
            ))}
        </div>
    );
};