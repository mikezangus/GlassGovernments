import React, { useState, useEffect } from "react";
import "./PanelCandidate.css";

export default function PanelCandidate ( {candidate, totalRaised } ) {
    const [donationsByType, setDonationsByType] = useState([]);
    useEffect(() => {
        if (candidate) {
            const fetchDonationsByType = async () => {
                const queryParams = new URLSearchParams({
                    firstName: candidate._id.firstName,
                    lastName: candidate._id.lastName,
                    party: candidate._id.party,
                    state: candidate._id.state,
                    district: candidate._id.district,
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
                    <h1>{candidate._id.firstName} {candidate._id.lastName}</h1>
                    <h2>{candidate._id.party}, {candidate._id.state}-{candidate._id.district}</h2>
                    <h3 key="totalRaised">Total raised: ${totalRaised.toLocaleString()}</h3>
                    <li>
                        {donationsByType.map((donation) => (
                            <li key={donation._id}>
                                {donation._id}: ${donation.totalAmount.toLocaleString()} | {((donation.totalAmount/totalRaised) * 100).toFixed(0)}%
                            </li>
                        ))}
                    </li>
                    
                </div>
            )}
        </div>
    );
};