import React from "react";
import formatCurrency from "../utilities/formatCurrency";
import calculatePercentage from "../utilities/calculatePercentage";


export default function RenderClusters({ candidate, centroids, cities, groups }) {

    const { totalContributionAmount } = candidate;

    return (
        <>
            {Object.keys(groups).map(clusterId => (
                <div key={clusterId}>
                    <h3>
                        Cluster {clusterId}
                    </h3>
                    <div>
                        <p>
                            Location: {cities[clusterId] || "Location currently unavailable"}
                        </p>
                        <p>
                            Cash: {formatCurrency(groups[clusterId].contributionAmount)}, {calculatePercentage(groups[clusterId].contributionAmount, totalContributionAmount)}%
                        </p>
                        <p>
                            Contributions: {groups[clusterId].contributionCount}
                        </p>
                    </div>
                </div>
            ))}
        </>
    );
};