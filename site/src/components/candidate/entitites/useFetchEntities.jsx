import { useEffect } from "react";


export default function useFetchEntities(chamber, state, district, candidate, setEntities) {
    const name = "Fetch Entities Hook"
    const fetchEntities = async () => {
        try {
            const { _id: { firstName, lastName, party } } = candidate;
            const params = new URLSearchParams(
                { chamber, state, district, firstName, lastName, party }
            );
            const url = `http://localhost:4000/api/candidate/entities?${params.toString()}`;
            const response = await fetch(url);
            if (!response.ok) throw new Error(`${name} | Network response was not ok`);
            const data = await response.json();
            const sortedData = data.sort(
                (a, b) => b.entityContributionAmount - a.entityContributionAmount
            );
            setEntities(sortedData);
        } catch (error) {
            console.error(`${name} | Error: `, error);
            setEntities([])
        };
    };
    useEffect(() => {
        if (chamber && state && district && candidate) fetchEntities();
    }, [chamber, state, district, candidate]);
};