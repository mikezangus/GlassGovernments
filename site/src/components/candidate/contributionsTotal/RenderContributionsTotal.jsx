import React from "react";
import formatCurrency from "../../../lib/formatCurrency";
import styles from "../../../styles/Candidate.module.css";


export default function RenderContributionsTotal({ totalContAmt }) {
    return (
        <div className={styles.contributions}>
            <div className={styles.total}>
                Total Raised: {formatCurrency(totalContAmt)}
            </div>
        </div>
    );
};
