import React, { useState, useEffect } from "react";
import "./PanelCandidate.css";

export default function PanelCandidate ( {candidate} ) {
    const [donationsByType, setDonationsByType] = useState([]);
    useEffect(() => {
        if (candidate) {
            const fetchDonationsByType = async () => {
                const queryParams = new URLSearchParams({
                    firstName: candidate._id.firstName,
                    lastName: candidate._id.lastName
                }).toString();
                const response = await fetch(`http://localhost:4000/api/candidate-panel?${queryParams}`);
                if (!response.ok) {
                    throw new Error("Nework response was not ok")
                }
                const data = await response.json();
                setDonationsByType(data);
            };
            fetchDonationsByType();
        }
    }, [candidate]);
    return (
        <div className={`panel-candidate ${candidate ? "white-background" : ""}`}>
            {candidate && (
                <div className="candidate-info">
                    <h3>{candidate._id.lastName}</h3>
                    <ul>
                        {donationsByType.map((donation) => (
                            <li key={donation._id}>
                                {donation._id}: ${donation.totalAmount.toLocaleString()}
                            </li>
                        ))}
                    </ul>
                    
                </div>
            )}
        </div>
    );
};