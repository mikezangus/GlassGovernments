import React from "react";
import "../../../css/switch.css";


export default function RenderOffices({ offices, defaultOffice, handleOfficeClick }) {

    const officeNames = {
        H: "House",
        P: "Presidency",
        S: "Senate"
    };
    
    return (
        <div className="switch">
            <div className="buttons-container">
                {offices.map((office) => (
                        <button
                            key={office}
                            className={`button ${defaultOffice === office ? "active" : ""}`}
                            onClick={() => handleOfficeClick(office)}
                        >
                            {officeNames[office] || office}
                        </button>
                    ))}
            </div>
        </div>
    );
};