import React from "react";
import formatCurrency from "../utilities/formatCurrency";
import calculatePercentage from "../utilities/calculatePercentage";


export default function RenderClusters({ candidate, centroids, groups }) {

    const { totalContributionAmount } = candidate;
    console.log(totalContributionAmount)

    return (
        <>
            {Object.keys(groups).map(clusterId => (
                <div key={clusterId}>
                    <h3>
                        Cluster {clusterId}
                    </h3>
                    {centroids[clusterId] &&
                        <div>
                            <p>
                                Centroid: Lat {centroids[clusterId].coordinates[1]}, Lng {centroids[clusterId].coordinates[0]}
                            </p>
                            <p>
                                Cash: {formatCurrency(groups[clusterId].contributionAmount)}, {calculatePercentage(groups[clusterId].contributionAmount, totalContributionAmount)}%
                            </p>
                            <p>
                                Contributions: {groups[clusterId].contributionCount}
                            </p>
                        </div>
                    }
                </div>
            ))}
        </>
    );
};