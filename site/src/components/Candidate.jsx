import React, { useState, useEffect } from "react";
import "../css/panel.css";
import { MapContainer, TileLayer } from "react-leaflet";


function getPartyColor (party) {
    switch (party) {
        case "DEMOCRATIC": return "darkblue";
        case "GREEN": return "darkgreen";
        case "INDEPENDENT": return "purple";
        case "LIBERTARIAN": return "gold";
        case "REPUBLICAN": return "darkred";
        default: return "gray";
    }
};


function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount);
};


function sortEntities(entities) {
    return entities.sort((a, b) => b.entityContributionAmount - a.entityContributionAmount);
};

function calculatePercentage(part, total) {
    return (part / total * 100).toFixed(2);
};


function createHeatmap ({ data }) {

}


export default function DisplayCandidate ({ chamber, state, district, candidate }) {

    const { _id: { firstName, lastName, party }, totalContributionAmount } = candidate;
    const [entityContributions, setEntityContributions] = useState([]);

    const fetchEntityContributions = async () => {
        try {
            const params = new URLSearchParams({
                chamber: chamber,
                state: state,
                district: district,
                firstName: firstName,
                lastName: lastName,
                party: party
            });
            const url = `http://localhost:4000/api/candidate?${params.toString()}`;
            const response = await fetch(url);
            if (!response.ok) throw new Error("Network response for display candidate was not ok")
            const data = await response.json();
            const sortedData = sortEntities(data)
            setEntityContributions(sortedData);
        } catch (error) {
            console.error("Error fetching candidate data: ", error);
            setEntityContributions([]);
        }
    }

    useEffect(() => {
        if (chamber && state && district && candidate) {
            fetchEntityContributions();
        }
    }, [chamber, state, district, candidate]);

    const partyColor = candidate ? getPartyColor(party) : "gray";

    return (
        <div className="panel">
            {candidate && (
                <div className="info">
                    <h1>
                        {firstName} {lastName}
                    </h1>
                    <h2>
                        <span style={{ color: partyColor }}>
                            {party}
                        </span>
                        , {state}-{district}
                    </h2>
                    <h3>
                        Total: {formatCurrency(totalContributionAmount)}
                        {entityContributions.map((contribution, index) => (
                            <li key={index}>
                                {contribution._id}: {formatCurrency(contribution.entityContributionAmount)} | {calculatePercentage(contribution.entityContributionAmount, totalContributionAmount)}%
                            </li>
                        ))}
                    </h3>
                </div>
            )}
            {candidate && (
                <div className="map">
                    
                </div>
            )}
        </div>
    )
}