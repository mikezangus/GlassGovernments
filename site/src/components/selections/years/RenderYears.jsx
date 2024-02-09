import React from "react";
import "../../../css/switch.css";


export default function RenderYears({ years, defaultYear, handleYearClick }) {
    return (
        <div className="switch">
            <div className="buttons-container">
                {years.map((year) => (
                    <button
                        key={year}
                        className={`button ${defaultYear === year ? "active" : ""}`}
                        onClick={() => handleYearClick(year)}
                    >
                        {year}
                    </button>
                ))}
            </div>

        </div>
    );
};