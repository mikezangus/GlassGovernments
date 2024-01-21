import { useEffect } from "react";


export default function useFetchCities(centroids, setCities) {
    useEffect(() => {    
        const fetchCity = async (coordinates) => {
            try {
                const lat = coordinates[1];
                const lng = coordinates[0];
                const url = `https://cors-anywhere.herokuapp.com/https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`;
                const response = await fetch(url);
                if (!response.ok) throw new Error ("Fetch City | Network response was not ok");
                const data = await response.json();
                if (!data.address) return null;
                const city = data.address.city || data.address.town || data.address.village;
                const state = data.address.state;
                return city && state ? `${city}, ${state}` : city || state || null;
            } catch (error) {
                console.error("Fetch City | Error fetching data: ", error);
                return null;
            };
        };
        const fetchCities = async () => {
            const cities = {};
            for (const clusterId in centroids) {
                const coordinates = centroids[clusterId].coordinates;
                cities[clusterId] = await fetchCity(coordinates);
            };
            setCities(cities);
        };
        if (Object.keys(centroids).length > 0) fetchCities();
    }, [centroids, setCities]);
};