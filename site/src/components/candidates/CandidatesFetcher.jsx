import { useEffect } from "react";
import sortCandidates from "./CandidateSorter";


export default function useFetchCandidates(chamber, state, district, setCandidates) {
    useEffect(() => {
        const fetchCandidates = async () => {
            try {
                const params = new URLSearchParams(
                    { chamber, state, district }
                );
                const url = `http://localhost:4000/api/candidates?${params.toString()}`;
                const response = await fetch(url);
                if (!response.ok) throw new Error("Candidate Fetcher | Network response was not ok");
                const data = await response.json();
                const sortedData = sortCandidates(data);
                setCandidates(sortedData);
            } catch (error) {
                console.error("Candidate Fetcher | Error fetching data: ", error);
            };
        };
        if (chamber && state && district) {
            fetchCandidates();
        };
    }, [chamber, state, district]);
};