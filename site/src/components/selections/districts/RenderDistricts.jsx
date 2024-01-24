import React from "react";
import "../../../css/dropdown.css";


export default function RenderDistricts({ districts, selectedDistrict, isOpen, toggleDropdown, handleDistrictClick }) {
    return (
        <div className="dropdown">
            <button
                className={`button ${isOpen ? "active" : ""}`}
                onClick={toggleDropdown}
            >
                {
                    selectedDistrict
                        ? `District: ${selectedDistrict}`
                        : "Select a district ▽"
                }
            </button>
            {isOpen && (
                <div className="menu">
                    {districts.map((district) => (
                        <button
                            className="item"
                            key={district}
                            onClick={() => handleDistrictClick(district)}
                        >
                            {district}
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
};