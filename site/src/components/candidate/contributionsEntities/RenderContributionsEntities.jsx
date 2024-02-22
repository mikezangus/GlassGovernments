import React from "react";
import formatCurrency from "../../utilities/formatCurrency";
import calculatePercentage from "../../utilities/calculatePercentage";
import styles from "../../../styles/Candidate.module.css"


export default function RenderContributionsEntities({ totalContributionAmount, entities }) {
    return (
        <>
            {entities.map((contribution, index) => (
                <div className={styles.contributions}>
                    <div
                        className={styles.entities}
                        key={index}
                    >
                        {contribution._id}: {formatCurrency(contribution.entityContributionAmount)} | {calculatePercentage(contribution.entityContributionAmount, totalContributionAmount)}% of total
                    </div>
                </div>
            ))}
        </>
    );
};
