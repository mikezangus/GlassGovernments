import React from "react";
import colorParty from "../../utilities/colorParty";
import capitalizeWord from "../../utilities/capitalizeWord";
import formatConstituency from "../../utilities/formatConstituency";
import formatParty from "../../utilities/formatParty";
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
            <div className={styles.party-constituency}>
                <span style={{ color: partyColor }}>
                    {capitalizeWord(party)}
                </span>
                , {formatConstituency(state, district)}
            </div>
        </div>
    );
};
