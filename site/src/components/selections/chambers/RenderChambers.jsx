import React from "react";
import capitalizeWords from "../../utilities/capitalizeWords";
import "../../../css/switch.css";


export default function RenderChambers({ chambers, defaultChamber, handleChamberClick }) {
    return (
        <div className="switch">
            {chambers.map((chamber) => (
                <button
                    key={chamber}
                    className={`button ${defaultChamber === chamber ? "active" : ""}`}
                    onClick={() => handleChamberClick(chamber)}
                >
                    {capitalizeWords(chamber)}
                </button>
            ))}
        </div>
    );
};