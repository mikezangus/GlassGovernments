import React from "react";
import colorParty from "../../utilities/colorParty";
import "../../../css/candidate.css";
import capitalizeWords from "../../utilities/capitalizeWords";


export default function RenderBio({ state, district, candidate }) {
    const { _id: { firstName, lastName, party} } = candidate;
    const partyColor = candidate ? colorParty(party) : "gray";
    return (
        <div className="bio">
            <div className="name">
                {firstName} {lastName}
            </div>
            <div className="party-constituency">
                <span style={{ color: partyColor }}>
                    {capitalizeWords(party)}
                </span>
                , {state}-{district}
            </div>
        </div>
    );
};