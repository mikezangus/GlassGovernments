import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import "leaflet.heat"
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import * as turf from "@turf/turf";


function HeatmapLayer({ points }) {

    const map = useMap();

    useEffect(() => {

        if (!map) return;

        const heatmapLayer = L.heatLayer(points, {
            radius: 20,
            blur: 15,
            maxZoom: 17
        }).addTo(map);

        return () => {
           map.removeLayer(heatmapLayer);
        };
    }, [map, points]);

    return null;

};


export default function DisplayCandidateMap({ chamber, state, district, candidate }) {


    const { _id: { firstName, lastName, party } } = candidate;
    const [coordinates, setCoordinates] = useState([]);
    const [clusters, setClusters] = useState([]);


    const fetchCoordinateData = async () => {
        try {
            const params = new URLSearchParams({
                chamber: chamber,
                state: state,
                district: district,
                firstName: firstName,
                lastName: lastName,
                party: party
            });
            const url = `http://localhost:4000/api/candidatemap?${params.toString()}`;
            const response = await fetch(url);
            if (!response.ok) throw new Error("Network response for display candidate info was not ok")
            const data = await response.json();
            const validData = data.filter(
                item => item.lat != null && item.lng != null
            );
            setCoordinates(validData);
        } catch (error) {
            console.error("Error fetching candidate data: ", error);
            setCoordinates([]);
        };
    };

    useEffect(() => {
        if (chamber && state && district && candidate) {
            fetchCoordinateData();
        }
    }, [chamber, state, district, candidate]);


    const clusterCoordinates = () => {
        const points = coordinates.map(
            coord => turf.point([coord.lng, coord.lat])
        );
        const featureCollection = turf.featureCollection(points);
        const clustered = turf.clustersDbscan(
            featureCollection,
            8046.72,
            { units: "meters" }
        );
        setClusters(clustered.features);
    };

    useEffect(() => {
        if (coordinates.length > 0) {
            clusterCoordinates();
        }
    }, [coordinates]);

    const groupClusters = () => {
        return clusters.reduce((acc, feature) => {
            const clusterId = feature.properties.cluster;
            if (!acc[clusterId]) {
                acc[clusterId] = [];
            }
            acc[clusterId].push(feature);
            return acc;
        }, {});
    };

    const calculateCentroids = () => {

        const centroids = {};

        clusters.forEach(cluster => {
            const clusterId = cluster.properties.cluster;
            if (clusterId !== undefined && !centroids[clusterId]) {
                const pointsInCluster = clusters.filter(
                    c => c.properties.cluster === clusterId
                );
                if (pointsInCluster.length > 0){
                    const featureCollection = turf.featureCollection(
                        pointsInCluster.map(
                            p => turf.point(p.geometry.coordinates)
                        )
                    );
                    const centroid = turf.centroid(featureCollection);
                    centroids[clusterId] = centroid.geometry.coordinates;
                }
            }
        });

        return centroids;
    }

    const renderClustersAsText = () => {
        const centroids = calculateCentroids();
        const grouped = groupClusters();
        return (
            <>
                {Object.keys(grouped).map(clusterId => (
                    <div key={clusterId}>
                        <h3>Cluster {clusterId}</h3>
                        {centroids[clusterId] &&
                            <p>Centroid: Lat {centroids[clusterId][1]}, Lng {centroids[clusterId][0]}</p>

                        }
                    </div>
                ))}
            </>
        );
    };


    const position = [39.8282, -98.5696];
    const heatmapPoints = coordinates
        .filter(coord => coord.lat != null && coord.lng != null)
        .map(coord => [coord.lat, coord.lng, coord.amount]);

    return (
        <div>
            <div>
                <h2>Clusters</h2>
                {renderClustersAsText()}
            </div>

            <MapContainer
            key={`${chamber}-${state}-${district}-${firstName}-${lastName}`}
                center={position}
                zoom={4}
                style={{
                    height: "500px",
                    width: "100%"
                }}
            >

                <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />

                {heatmapPoints.length > 0 && 

                    <HeatmapLayer
                        points={heatmapPoints}
                    />
                }

            </MapContainer>
        </div>
    );
};