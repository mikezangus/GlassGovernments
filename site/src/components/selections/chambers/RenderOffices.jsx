import React from "react";
import capitalizeWords from "../../utilities/capitalizeWords";
import "../../../css/switch.css";


export default function RenderOffices({ offices, defaultOffice, handleOfficeClick }) {
    return (
        <div className="switch">
            {offices.map((office) => (
                <button
                    key={office}
                    className={`button ${defaultOffice === office ? "active" : ""}`}
                    onClick={() => handleOfficeClick(office)}
                >
                    {capitalizeWords(office)}
                </button>
            ))}
        </div>
    );
};