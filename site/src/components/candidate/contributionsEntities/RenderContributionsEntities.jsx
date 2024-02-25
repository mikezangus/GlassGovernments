import React from "react";
import formatCurrency from "../../utilities/formatCurrency";
import calculatePercentage from "../../utilities/calculatePercentage";
import styles from "../../../styles/Candidate.module.css"


export default function RenderContributionsEntities({ totalContAmt, entities }) {
    return (
        <>
            {entities.map((contribution, index) => (
                <div className={styles.contributions}>
                    <div
                        className={styles.entities}
                        key={index}
                    >
                        {contribution._id}: {formatCurrency(contribution.entityContAmt)} | {calculatePercentage(contribution.entityContAmt, totalContAmt)}% of total
                    </div>
                </div>
            ))}
        </>
    );
};
