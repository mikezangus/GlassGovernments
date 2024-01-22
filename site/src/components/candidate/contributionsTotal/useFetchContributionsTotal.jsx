import { useEffect } from "react";


export default function useFetchContributionsTotal(chamber, state, district, candidate) {
    const name = "Fetch Contributions Total Hook"
    const fetchContributionsTotal = async () => {
        try {
            const { _id: { firstName, lastName, party } } = candidate;
            const params = new URLSearchParams(
                { chamber, state, district, firstName, lastName, party }
            );
            const url = `http://localhost:4000/api/candidate/contributions/total?${params.toString()}`;
            const response = await fetch(url);
            if (!response.ok) throw new Error(`${name} | Network response was not ok`);
            const data = await response.json();
            return data
        } catch (error) {
            console.error(`${name} | Error: `, error);
        };
    };
    useEffect(() => {
        if (chamber && state && district && candidate) fetchContributionsTotal();
    }, [chamber, state, district, candidate]);
};