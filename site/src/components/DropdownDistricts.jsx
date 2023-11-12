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

    const handleDistrictClick = (districtObject) => {
        
        const state = districtObject._id.state;
        const districtNumber = districtObject._id.district;
        onSelectedDistrict({ state, district: districtNumber});
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
                        {districts.map(district => {
                            const keyId = `${district._id.state}-${district._id.district}`;
                            return (
                                <button
                                    className="dropdown__item"
                                    key={keyId}
                                    onClick={() => handleDistrictClick(district)}
                                >
                                    {district._id.state}-{district._id.district}
                                </button>
                            );
                        })}
                    </div>
                )}
            </div>
        </main>
    );
};