import React, { useState, useEffect } from "react";
import "../css/dropdown.css";


export default function SelectDistrict({ selectedChamber, selectedState, onDistrictSelect, selectedDistrict }) {

    const [districts, setDistricts] = useState([]);
    const [isOpen, setIsOpen] = useState(false);

    const fetchDistricts = async () => {
        try {
            const response = await fetch(`http://localhost:4000/api/districts?state=${encodeURIComponent(selectedState)}&chamber=${encodeURIComponent(selectedChamber)}`);
            if (!response.ok) throw new Error("Network response for districts endpoint was not ok");
            const data = await response.json();
            setDistricts(data);
        } catch (error) {
            console.error("Error fetching districts data ", error)
        }
    };

    useEffect(() => {
        if (selectedChamber && selectedState) {
            fetchDistricts();
        }
    }, [selectedChamber, selectedState]);

    const handleDistrictClick = (district) => {
        onDistrictSelect(district);
        setIsOpen(false);
    };

    const toggleDropdown = () => setIsOpen(!isOpen);

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