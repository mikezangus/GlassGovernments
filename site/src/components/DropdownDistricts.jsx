import React, { useState, useEffect } from "react";
import "./Dropdown.css";

export default function DropdownDistricts({ onSelectedDistrict }) {

    const [districts, setDistricts] = useState([]);
    const [isOpen, setIsOpen] = useState(false);

    const fetchDistricts = async () => {
        try {
            const response = await fetch("http://localhost:4000/api/districts");
            if (!response.ok) throw new Error("Network response was not ok");
            const data = await response.json();
            setDistricts(data);
        } catch (error) {
            console.error("Error fetching data", error);
        }
    };
    useEffect(() => {
        fetchDistricts();
    }, []);

    const handleDistrictClick = (district) => {
        onSelectedDistrict(district);
        setIsOpen(false);
    };

    const toggleDropdown = () => setIsOpen(!isOpen);

    return (
        <main>
            <div className="dropdown">
                <h2 className="dropdown__title">Districts</h2>
                <button className="dropdown__button" onClick={toggleDropdown}>
                    Click to select a district
                </button>
                {isOpen && (
                    <div className="dropdown__menu" style={{ display: "block" }}>
                        {districts.map((districtObject, index) => {
                            const districtString = `${districtObject._id.state}-${districtObject._id.district}`;
                            return (
                                <button
                                    className="dropdown__item"
                                    key={index}
                                    onClick={() => handleDistrictClick(districtString)}
                                >
                                    {districtString}
                                </button>
                            );
                        })}
                    </div>
                )}
            </div>
        </main>
    );
};