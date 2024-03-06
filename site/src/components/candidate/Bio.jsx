import React, { useEffect, useState } from "react";
import formatParty from "../../lib/formatParty";
import capitalizeWord from "../../lib/capitalizeWord";
import formatConstituency from "../../lib/formatConstituency";
import colorParty from "../../lib/colorParty";
import styles from "../../styles/candidate/Bio.module.css";
import formatCurrency from "../../lib/formatCurrency";


function Renderer({ state, district, candidate }) {

    const [isMobile, setIsMobile] = useState(window.innerWidth < 768);
    useEffect(() => {
        const handleResize = () => {
            setIsMobile(window.innerWidth < 768);
        };
        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize", handleResize);
    }, []);

    let { name, party, amt } = candidate;
    party = formatParty(party)
    const partyColor = candidate ? colorParty(party) : "gray";

    return (

        <div className={styles.bio}>

            <div className={styles.name}>
                {name}
            </div>

            <div className={styles.partyConstituencyContainer}>
                <div
                    className={styles.party}
                    style={{ color: partyColor }}
                >
                    {capitalizeWord(party)}
                </div>

                <div className={styles.constituency}>
                    {isMobile
                        ? ""
                        : ", "
                    }
                    {formatConstituency(state, district)}
                </div>

            </div>

            <div className={styles.amt}>
                Total Raised: {formatCurrency(amt)}
            </div>

        </div>

    );

}


export default function Bio({ state, district, candidate }) {
    return (
        <Renderer
            state={state}
            district={district}
            candidate={candidate}
        />
    );
};
