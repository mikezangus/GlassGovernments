import { useEffect } from "react";


export default function useFetchCoordinates(chamber, state, district, candidate, setCoordinates) {
    const name = "Fetch Coordinates Hook"
    const fetchCoordinates = async () => {
        try {
            const { _id: { firstName, lastName, party } } = candidate;
            const params = new URLSearchParams(
                { chamber, state, district, firstName, lastName, party }
            );
            const url = `http://localhost:4000/api/candidate/coordinates?${params.toString()}`;
            const response = await fetch(url);
            if (!response.ok) throw new Error(`${name} | Network response was not ok`);
            const data = await response.json();
            const filteredData = data.filter(
                item => item.lat != null && item.lng != null
            );
            setCoordinates(filteredData);
        } catch (error) {
            console.error(`${name} | Error fetching data: ${error}`);
            setCoordinates([]);
        };
    };
    useEffect(() => {
        if (chamber && state && district && candidate) fetchCoordinates();
    }, [chamber, state, district, candidate]);
};