import React, { useState, useEffect } from "react";
import "./Dropdown.css";

export default function DropdownDistricts({ onSelectedDistrict, selectedDistrict }) {

    const [districts, setDistricts] = useState([]);
    const [isOpen, setIsOpen] = useState(false);

    const sortDistricts = (districtArray) => {
        return districtArray.sort((a, b) => {
            const stateA = a._id.state, districtA = parseInt(a._id.district, 10);
            const stateB = b._id.state, districtB = parseInt(b._id.district, 10);
            if (stateA < stateB) return -1;
            if (stateA > stateB) return 1;
            return districtA - districtB;
        });
    };

    const fetchDistricts = async () => {
        try {
            const response = await fetch("http://localhost:4000/api/districts");
            if (!response.ok) throw new Error("Network response was not ok");
            const data = await response.json();
            const sortedData = sortDistricts(data)
            setDistricts(sortedData);
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

    const toggleDropdown = () => {
        console.log("Districts dropdown button clicked");
        setIsOpen(!isOpen);
    };

    return (
        <div className="dropdown">
            <h2 className="dropdown__title">Districts</h2>
            <button className="dropdown__button" onClick={toggleDropdown}>
                {selectedDistrict ? `District selected: ${selectedDistrict}` : "Click to select a district"}
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
    );
};