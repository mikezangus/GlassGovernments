import { useState } from "react";
import useFetchCoordinates from "./useFetchCoordinates";
import useCreateCluster from "./useCreateCluster";
import groupClusters from "./groupClusters";
import calculateCentroids from "./calculateCentroids";
import useFetchCities from "./useFetchCities";
import RenderClusters from "./RenderClusters";


export default function ShowClusters({ chamber, state, district, candidate }) {

    const [coordinates, setCoordinates] = useState([]);
    const [clusters, setClusters] = useState([]);
    const [cities, setCities] = useState([]);

    useFetchCoordinates(chamber, state, district, candidate, setCoordinates);
    useCreateCluster(coordinates, setClusters);

    const groups = groupClusters(clusters);
    const centroids = calculateCentroids(clusters);
    useFetchCities(centroids, setCities);

    return (
        <RenderClusters
            candidate={candidate}
            centroids={centroids}
            cities={cities}
            groups={groups}
        />
    );
};