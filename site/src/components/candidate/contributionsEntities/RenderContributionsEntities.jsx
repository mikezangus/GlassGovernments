import React from "react";
import formatCurrency from "../../utilities/formatCurrency";
import calculatePercentage from "../../utilities/calculatePercentage";
import "../../../css/candidate.css";
import capitalizeWords from "../../utilities/capitalizeWords";


export default function RenderContributionsEntities({ candidate, entities }) {
    const { totalContributionAmount } = candidate;
    return (
        <>
            {entities.map((contribution, index) => (
                <div className="contributions">
                    <div className="entities" key={index}>
                        {capitalizeWords(contribution._id)}: {formatCurrency(contribution.entityContributionAmount)} | {calculatePercentage(contribution.entityContributionAmount, totalContributionAmount)}%
                    </div>
                </div>
            ))}
        </>
    );
};