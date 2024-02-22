import React from "react";
import formatCurrency from "../../utilities/formatCurrency";
import styles from "../../../styles/Candidate.module.css";


export default function RenderContributionsTotal({ totalContributionAmount }) {
    return (
        <div className={styles.contributions}>
            <div className={styles.total}>
                Total Raised: {formatCurrency(totalContributionAmount)}
            </div>
        </div>
    );
};
