import React from "react";
import "../../../css/panel.css";
import formatCurrency from "../utilities/formatCurrency";
import calculatePercentage from "../utilities/calculatePercentage";


export default function RenderContributionsEntities({ candidate, entities }) {
    const { totalContributionAmount } = candidate;
    return (
        <div className="panel">
            <div className="info">
                    {entities.map((contribution, index) => (
                        <h4 key={index}>
                            {contribution._id}: {formatCurrency(contribution.entityContributionAmount)} | {calculatePercentage(contribution.entityContributionAmount, totalContributionAmount)}%
                        </h4>
                    ))}
            </div>
        </div>
    );
};