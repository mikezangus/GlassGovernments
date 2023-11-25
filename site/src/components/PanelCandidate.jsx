import React, { useState, useEffect } from "react";
import "./PanelCandidate.css";

export default function PanelCandidate({ candidate, totalRaised }) {

    const [donationsByType, setDonationsByType] = useState([]);
    const [donationHotspots, setDonationHotspots] = useState([]);

    useEffect(() => {
        if (candidate) {
            console.log("Current candidate:", candidate);
            fetchDonationsByType();
            fetchDonationHotspots();
        }
    }, [candidate]);

    const getPartyColor = (party) => {
        switch (party) {
            case "DEMOCRATIC":
                return "darkblue";
            case "REPUBLICAN":
                return "darkred";
            case "LIBERTARIAN":
                return "gold";
            case "GREEN":
                return "darkgreen";
            default:
                return "gray";
        }
    };

    const fetchDonationsByType = async () => {
        try {
            const typeResponse = await fetch(
                `http://localhost:4000/api/funding-by-entity?${new URLSearchParams({
                    firstName: candidate._id.firstName,
                    lastName: candidate._id.lastName,
                    state: candidate._id.state,
                    district: candidate._id.district,
                }).toString()}`
            );
            if (!typeResponse.ok) {
                throw new Error("Network response was not ok for donations by entity type");
            }
            const typeData = await typeResponse.json();
            setDonationsByType(typeData);
        } catch (error) {
            console.error("Error fetching data", error);
        }
    };

    const fetchDonationHotspots = async () => {
        const queryParams = new URLSearchParams({
            state: candidate._id.state,
            district: candidate._id.district,
            lastName: candidate._id.lastName,
            firstName: candidate._id.firstName
        }).toString();
        console.log("Query paramters for hotspots:", queryParams)
        try {
            const response = await fetch(`http://localhost:4000/api/funding-by-location?${queryParams}`);
            if (!response.ok) {
                throw new Error("Network response was not ok")
            }
            const hotspots = await response.json();
            console.log("Fetched donation hotspots:", hotspots);
            setDonationHotspots(hotspots);
        } catch (error) {
            console.error("Error fetching donation hotspots:", error);
        }
    };

    const partyColor = candidate ? getPartyColor(candidate._id.party) : "gray";

    return (
        <div className={`panel-candidate ${candidate ? "white-background" : ""}`}>
            {candidate && (
                <div className="candidate-info">
                    <h1>{candidate._id.firstName} {candidate._id.lastName}</h1>
                    <h2>
                        <span style={{ color: partyColor }}>
                            {candidate._id.party}
                        </span>
                        , {candidate._id.state}-{candidate._id.district}
                    </h2>
                    <h3 key="totalRaised">Total raised: ${totalRaised.toLocaleString()}</h3>
                    <ul>
                        {donationsByType.map((donation) => (
                            <li key={donation._id}>
                                {donation._id}: ${donation.totalAmount.toLocaleString()} | {((donation.totalAmount / totalRaised) * 100).toFixed(0)}%
                            </li>
                        ))}
                    </ul>
                    <section>
                        <h3>Donation spots</h3>
                        <ul>
                            {donationHotspots.map((geo, index) => (
                                <li key={index}>
                                    Lat: {geo.latitude}, Lng: {geo.longitude}
                                </li>
                            ))}
                        </ul>
                    </section>
                </div>
            )}
        </div>
    );
};