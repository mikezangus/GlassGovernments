import { useEffect } from "react";


export default function useFetchCoordinates(chamber, state, district, candidate, setCoordinates) {
    useEffect(() => {
        const fetchCoordinates = async () => {
            try {
                const { _id: { firstName, lastName, party } } = candidate;
                const params = new URLSearchParams(
                    { chamber, state, district, firstName, lastName, party }
                );
                const url = `http://localhost:4000/api/candidate/coordinates?${params.toString()}`;
                const response = await fetch(url);
                if (!response.ok) throw new Error("Fetch Coordinates Hook | Network response was not ok");
                const data = await response.json();
                const validData = data.filter(
                    item => item.lat != null && item.lng != null
                );
                setCoordinates(validData);
            } catch (error) {
                console.error("Fetch Coordinates Hook | Error: ", error);
                setCoordinates([]);
            };
        };
        if (chamber && state && district && candidate) fetchCoordinates();
    }, [chamber, state, district, candidate]);
};