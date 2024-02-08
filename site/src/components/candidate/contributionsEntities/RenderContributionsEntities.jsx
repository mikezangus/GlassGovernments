import React from "react";
import formatCurrency from "../../utilities/formatCurrency";
import calculatePercentage from "../../utilities/calculatePercentage";
import "../../../css/candidate.css";
import capitalizeWord from "../../utilities/capitalizeWord";


export default function RenderContributionsEntities({ totalContributionAmount, entities }) {
    return (
        <>
            {entities.map((contribution, index) => (
                <div className="contributions">
                    <div className="entities" key={index}>
                        {contribution._id}: {formatCurrency(contribution.entityContributionAmount)} | {calculatePercentage(contribution.entityContributionAmount, totalContributionAmount)}% of total
                    </div>
                </div>
            ))}
        </>
    );
};