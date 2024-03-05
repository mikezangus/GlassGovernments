import React from "react";
import colorParty from "../../../lib/colorParty";
import capitalizeWord from "../../../lib/capitalizeWord";
import formatConstituency from "../../../lib/formatConstituency";
import formatParty from "../../../lib/formatParty";
import styles from "../../../styles/Candidate.module.css";


export default function RenderBio({ state, district, candidate }) {
    let { name, party } = candidate;
    party = formatParty(party)
    const partyColor = candidate ? colorParty(party) : "gray";
    return (
        <div className={styles.bio}>
            <div className={styles.name}>
                {name}
            </div>
            <div className={styles.partyConstituency}>
                <div style={{ color: partyColor }}>
                    {capitalizeWord(party)}
                </div>
                <div>
                {formatConstituency(state, district)}
                </div>
            </div>
        </div>
    );
};
