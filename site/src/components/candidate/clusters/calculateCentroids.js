import * as turf from "@turf/turf";


export default function calculateCentroids(clusters) {
    console.log("Clusters: ", clusters)
    const centroids = {};
    clusters.forEach(cluster => {
        const clusterId = cluster.properties.cluster;
        if (clusterId !== undefined && !centroids[clusterId]) {
            const pointsInCluster = clusters.filter(
                c => c.properties.cluster === clusterId
            );
            if (pointsInCluster.length > 0) {
                const featureCollection = turf.featureCollection(
                    pointsInCluster.map(p => turf.point(p.geometry.coordinates))
                );
                const centroid = turf.centroid(featureCollection);
                const clusterAmount = pointsInCluster.reduce(
                    (sum, point) => sum + (point.properties.amount), 0
                );
                centroids[clusterId] = {
                    coordinates: centroid.geometry.coordinates,
                    clusterAmount: clusterAmount
                };
            };
        };
    });
    return centroids;
};