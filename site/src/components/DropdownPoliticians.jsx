import React, { useState, useEffect } from "react";
import "./Dropdown.css";

function formatAmount(amount) {
    return (
        amount >= 10000000 ? `${(amount / 1000000).toFixed(1)}M` : // $60,900,000 => $60.9M
        amount >= 1000000 ? `${(amount / 1000000).toFixed(2)}M` : // $6,090,000 => $6.09M
        amount >= 100000 ? `${(amount / 1000).toFixed(0)}K` : // $609,000 => $609K
        amount >= 10000 ? `${(amount / 1000).toFixed(1)}K` : // $60,900 => $60.9K
        amount >= 1000 ? `${(amount / 1000).toFixed(2)}K` : // $6,090 => $6.09K
        `${amount}` // $609 => $609
    );
};

export default function DropdownPoliticians({ district }) {

    const [lastNames, setLastNames] = useState([]);
    const [isOpen, setIsOpen] = useState(false);

    const fetchLastNames = async () => {
        try {
            const queryParams = new URLSearchParams({
                state: district ? district.state : "",
                district: district ? district.district : ""
            }).toString();
            const response = await fetch(`http://localhost:4000/api/lastnames?${queryParams}`);
            if (!response.ok) throw new Error("Network response was not ok");
            const data = await response.json();
            setLastNames(data);
        } catch (error) {
            console.error("Error fetching data", error);
        }
    };
    useEffect(() => {
        if (district) {
            fetchLastNames();
        }
    }, [district]);

    const toggleDropdown = () => setIsOpen(!isOpen);

    return (
        <main>
            <div className="dropdown">
                <h2 className="dropdown__title">Politicians from {district && district._id ? `${district._id.state}-${district._id.district}` : ""} </h2>
                <button className="dropdown__button" onClick={toggleDropdown}>
                    Click to select a politician
                </button>
                {isOpen && (
                    <div className="dropdown__menu" style={{ display: "block" }}>
                        {lastNames.map((lastName) => {
                            const keyId = `${lastName._id.lastName}-${lastName._id.state}-${lastName._id.district}`;
                            return (
                                <button
                                    className="dropdown__item"
                                    key={keyId}
                                    onClick={() => setIsOpen(false)}
                                >
                                    {lastName._id.lastName} ({lastName._id.state}-{lastName._id.district}) - ${formatAmount(lastName.totalFunding)}
                                </button>
                            );
                        })}
                    </div>
                )}
            </div>
        </main>
    );
};