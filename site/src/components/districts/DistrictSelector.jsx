import React from "react";
import "../../css/dropdown.css";


export default function DistrictsDropdown(districts, selectedDistrict, isOpen, toggleDropdown, handleDistrictClick) {
    return (
        <div className="dropdown">
            <button className="dropdown__button" onClick={toggleDropdown}>
                {selectedDistrict ? `District selected: ${selectedDistrict}` : "Click to select a district"}
            </button>
            {isOpen && (
                <div className="dropdown__menu" style={{ display: "block" }}>
                    {districts.map((district) => (
                        <button
                            className="dropdown__item"
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