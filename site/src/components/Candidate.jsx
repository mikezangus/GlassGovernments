import React, { useState, useEffect } from "react";
import "../css/panel.css";


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
}


export default function DisplayCandidate ({ chamber, state, district, candidate }) {

    const { firstName, lastName, party } = candidate;
    const [entityContributions, setEntityContributions] = useState([]);

    const fetchEntityContributions = async () => {
        try {
            const response = await fetch(`http://localhost:4000/api/candidate?chamber=${encodeURIComponent(chamber)}&state=${encodeURIComponent(state)}&district=${encodeURIComponent(district)}&firstName=${encodeURIComponent(firstName)}&lastName=${encodeURIComponent(lastName)}&party=${encodeURIComponent(party)}`);            console.log("Response: ", response)
            if (!response.ok) throw new Error("Network response for display candidate was not ok")
            const data = await response.json();
            console.log("Data via display candidate component: ", data);
            setEntityContributions(data);
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
        <div className={`panel-candidate ${candidate ? "white-background" : ""}`}>
            {candidate && (
                <div className="candidate-info">
                    <h1>
                        {firstName} {lastName}
                    </h1>
                    <h2>
                        <span style={{ color: partyColor }}>
                            {party}
                        </span>
                        , {state}-{district}
                    </h2>
                    <ul>
                        {entityContributions.map((contribution, index) => (
                            <li key={index}>
                                {contribution._id}: {contribution.entityContributionAmount}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    )
}