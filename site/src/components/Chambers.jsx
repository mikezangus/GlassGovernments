import React, { useState, useEffect } from "react";
import "../css/switch.css";

export default function SelectChamber({ onChamberSelect }) {

    const [chambers, setChambers] = useState([]);
    const [defaultSelectedChamber, setDefaultSelectedChamber] = useState(null);

    const fetchChambers = async () => {
        try {
            const url = "http://localhost:4000/api/chambers";
            const response = await fetch(url);
            if (!response.ok) throw new Error("Network response for chambers endpoint was not ok");
            const data = await response.json();
            setChambers(data);
            if (data.length > 0) {
                const defaultChamber = data[0];
                setDefaultSelectedChamber(defaultChamber);
                onChamberSelect(defaultChamber);
            }
        } catch (error) {
            console.error("Chambers.jsx — Error fetching data: ", error)
        }
    };

    useEffect(() => {
        fetchChambers();
    }, []);

    const handleChamberClick = (chamber) => {
        setDefaultSelectedChamber(chamber);
        onChamberSelect(chamber);
    };

    return (
        <div className="switch-container">
            {chambers.map((chamber) => (
                <button
                    key={chamber}
                    className={`switch-button ${defaultSelectedChamber === chamber ? "active" : ""}`}
                    onClick={() => handleChamberClick(chamber)}
                >
                    {chamber}
                </button>
            ))}
        </div>
    );
};