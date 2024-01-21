import { useEffect } from "react";
import * as turf from "@turf/turf";


export default function useCreateCluster(coordinates, setClusters) {
    useEffect(() => {
        const createCluster = () => {

            const points = coordinates.map(coord => {
                const point = turf.point([coord.lng, coord.lat]);
                point.properties.amount = coord.amount;
                return point;
            });
            const featureCollection = turf.featureCollection(points);
            const clustered = turf.clustersDbscan(featureCollection, 8046.72, { units: "meters" });

            const clusterSums = {};
            clustered.features.forEach(feature => {
                const clusterId = feature.properties.cluster;
                const amount = feature.properties.amount || 0;
                if (clusterId !== undefined) {
                    if (!clusterSums[clusterId]) clusterSums[clusterId] = 0;
                    clusterSums[clusterId] += amount;
                };
            });

            clustered.features.forEach(feature => {
                const clusterId = feature.properties.cluster;
                if (clusterId !== undefined) feature.properties.totalAmount = clusterSums[clusterId];
            });

            setClusters(clustered.features);

        };
        if (coordinates.length > 0) createCluster();
    }, [coordinates]);
};