import React from "react";
import "../../../css/panel.css";
import colorParty from "../utilities/colorParty";


export default function RenderBio({ state, district, candidate }) {
    const { _id: { firstName, lastName, party} } = candidate;
    const partyColor = candidate ? colorParty(party) : "gray";
    return (
        <div className="panel">
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
            </div>
        </div>
    );
};