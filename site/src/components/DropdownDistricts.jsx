import React, { useState, useEffect, useRef } from "react";
import "./Dropdown.css";

export default function DropdownDistricts() {
    const [isOpen, setIsOpen] = useState(false);
    const [districts, setDistricts] = useState([]);
    const dropdownRef = useRef(null);
    useEffect(() => {
        fetch("http://localhost:4000/api/districts")
            .then(response => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then(data => setDistricts(data))
            .catch(error => console.error("Error fetchind data:", error));
    }, []);

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setIsOpen(false);
            }
        };
        if (isOpen) {
            document.addEventListener("mousedown", handleClickOutside);
        };
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, [isOpen]);
    const toggleDropdown = () => {
        setIsOpen(prevState => !prevState)
    };
    return (
        <main>
            <div className="list-container">
                <h2 className="list-title">Districts</h2>
                <div className="dropdown" ref={dropdownRef}>
                    <button onClick={toggleDropdown}>
                        Click to select a district
                    </button>
                    {isOpen && (
                        <div className="dropdown-menu">
                            {districts.map(district => (
                                <button
                                    key={`${district._id.state}-${district._id.district}`}
                                    onClick={() => setIsOpen(false)}
                                >
                                    {district._id.state}-{district._id.district}
                                </button>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </main>
    );
};