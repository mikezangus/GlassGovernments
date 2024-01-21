export default function groupClusters(clusters) {
    return (
        clusters.reduce((acc, feature) => {
            const clusterId = feature.properties.cluster;
            if (!acc[clusterId]) {
                acc[clusterId] = {
                    features: [],
                    contributionAmount: feature.properties.totalAmount || 0,
                    contributionCount: 0
                };
            };
            acc[clusterId].features.push(feature);
            acc[clusterId].contributionCount += 1;
            return acc;
        }, {})
    );
};