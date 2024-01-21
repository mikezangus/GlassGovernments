import { useState } from "react";
import useFetchCoordinates from "./useFetchCoordinates";
import useCreateCluster from "./useCreateCluster";
import groupClusters from "./groupClusters";
import calculateCentroids from "./calculateCentroids";
import RenderClusters from "./RenderClusters";


export default function ShowClusters({ chamber, state, district, candidate }) {
    const [coordinates, setCoordinates] = useState([]);
    const [clusters, setClusters] = useState([]);
    useFetchCoordinates(chamber, state, district, candidate, setCoordinates);
    useCreateCluster(coordinates, setClusters);
    console.log("Coordinates via component: ", coordinates)
    const groups = groupClusters(clusters);
    const centroids = calculateCentroids(clusters);
    const cities = null;
    return (
        <RenderClusters
            candidate={candidate}
            centroids={centroids}
            groups={groups}
        />
    );
};