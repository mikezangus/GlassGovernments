import React, { useEffect, useState } from "react";
import formatParty from "../../lib/formatParty";
import capitalizeWord from "../../lib/capitalizeWord";
import formatConstituency from "../../lib/formatConstituency";
import colorParty from "../../lib/colorParty";
import styles from "../../styles/candidate/Bio.module.css";
import formatCurrency from "../../lib/formatCurrency";
import useIsMobile from "../../lib/useIsMobile";


function RenderPartyAndConstituency({ partyRaw, candidate, state, district }) {

    const isMobile = useIsMobile();

    const party = formatParty(partyRaw)
    const partyColor = candidate ? colorParty(party) : "gray";

    return (
        <div className={styles.partyConstituencyContainer}>
            <div
                className={styles.party}
                style={{ color: partyColor }}
            >
                {capitalizeWord(party)}
            </div>
            <div className={styles.constituency}>
                { isMobile ? "" : ", " }
                {formatConstituency(state, district)}
            </div>
        </div>
    );
};


function Renderer({ state, district, candidate }) {
    const { name, party, amt } = candidate;
    return (
        <div className={styles.bio}>

            <div className={styles.name}>
                {name}
            </div>
            <RenderPartyAndConstituency
                partyRaw={party}
                candidate={candidate}
                state={state}
                district={district}
            />
            <div className={styles.amt}>
                Total Raised — {formatCurrency(amt)}
            </div>
        </div>
    );
};


export default function Bio({ state, district, candidate }) {
    return (
        <Renderer
            state={state}
            district={district}
            candidate={candidate}
        />
    );
};
