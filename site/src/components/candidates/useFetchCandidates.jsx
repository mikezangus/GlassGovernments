import { useEffect } from "react";
import sortCandidates from "./utilities/sortCandidates";


export default function useFetchCandidates(chamber, state, district, setCandidates) {
    const name = "Fetch Candidates Hook";
    const fetchCandidates = async () => {
        try {
            const params = new URLSearchParams( { chamber, state, district });
            const url = `http://localhost:4000/api/candidates?${params.toString()}`;
            const response = await fetch(url);
            if (!response.ok) throw new Error(`${name} | Network response was not ok`);
            const data = await response.json();
            const sortedData = sortCandidates(data);
            setCandidates(sortedData);
        } catch (error) {
            console.error(`${name} | Error: `, error);
        };
    };
    useEffect(() => {
        if (chamber && state && district) fetchCandidates();
    }, [chamber, state, district]);
};