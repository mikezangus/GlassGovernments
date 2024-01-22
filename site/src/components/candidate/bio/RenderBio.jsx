import React from "react";
import colorParty from "../utilities/colorParty";
import "../../../css/candidate.css";
import capitalize from "../utilities/capitalize";


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
                    {capitalize(party)}
                </span>
                , {state}-{district}
            </div>
        </div>
    );
};