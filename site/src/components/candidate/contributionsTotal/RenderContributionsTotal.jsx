import React from "react";
import formatCurrency from "../../utilities/formatCurrency";
import "../../../css/candidate.css";


export default function RenderContributionsTotal({ candidate }) {
    const { totalContributionAmount } = candidate;
    return (
        <div className="contributions">
            <div className="total">
                Total Raised: {formatCurrency(totalContributionAmount)}
            </div>
        </div>
    );
};