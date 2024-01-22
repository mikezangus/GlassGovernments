import React from "react";
import "../../../css/panel.css";
import formatCurrency from "../utilities/formatCurrency";


export default function RenderContributionsTotal({ candidate }) {
    const { totalContributionAmount } = candidate;
    return (
        <div className="panel">
            <div className="info">
                <h2>
                    Total Raised: {formatCurrency(totalContributionAmount)}
                </h2>
            </div>
        </div>
    );
};