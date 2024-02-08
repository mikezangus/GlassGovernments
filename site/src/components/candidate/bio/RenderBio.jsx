import React from "react";
import colorParty from "../../utilities/colorParty";
import "../../../css/candidate.css";
import capitalizeWords from "../../utilities/capitalizeWords";
import formatConstituency from "../../utilities/formatConstituency";
import formatParty from "../../utilities/formatParty";


export default function RenderBio({ state, district, candidate }) {
    let { totalContributionAmount, name, candID, party } = candidate;
    party = formatParty(party)
    const partyColor = candidate ? colorParty(party) : "gray";
    return (
        <div className="bio">
            <div className="name">
                {name}
            </div>
            <div className="party-constituency">
                <span style={{ color: partyColor }}>
                    {capitalizeWords(party)}
                </span>
                , {formatConstituency(state, district)}
            </div>
        </div>
    );
};