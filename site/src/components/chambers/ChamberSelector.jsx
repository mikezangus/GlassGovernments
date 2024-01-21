import React from "react";
import "../../css/switch.css";


export default function ChambersSwitch(chambers, defaultChamber, handleChamberClick) {
    return (
        <div className="switch-container">
            {chambers.map((chamber) => (
                <button
                    key={chamber}
                    className={`switch-button ${defaultChamber === chamber ? "active" : ""}`}
                    onClick={() => handleChamberClick(chamber)}
                >
                    {chamber}
                </button>
            ))}
        </div>
    )
};