import React from "react";
import "../../../css/panel.css";
import formatCurrency from "../utilities/formatCurrency";
import calculatePercentage from "../utilities/calculatePercentage";


export default function RenderEntities(candidate, entityContributions) {
    const { totalContributionAmount } = candidate;
    return (
        <div className="panel">
            <div className="info">
                    {entityContributions.map((contribution, index) => (
                        <li key={index}>
                            {contribution._id}: {formatCurrency(contribution.entityContributionAmount)} | {calculatePercentage(contribution.entityContributionAmount, totalContributionAmount)}%
                        </li>
                    ))}
            </div>
        </div>
    );
};