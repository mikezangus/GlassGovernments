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
                        ? `District: ${parseInt(selectedDistrict, 10).toString()}`
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
                            {`District ${parseInt(district, 10).toString()}`}
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
};