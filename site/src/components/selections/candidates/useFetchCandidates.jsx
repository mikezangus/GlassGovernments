import { useEffect } from "react";


export default function useFetchCandidates(year, chamber, state, district, setCandidates) {
    const name = "Fetch Candidates Hook";
    const fetchCandidates = async () => {
        try {
            const params = new URLSearchParams( { chamber, state, district });
            const url = `http://localhost:4000/api/candidates?${params.toString()}`;
            const response = await fetch(url);
            if (!response.ok) throw new Error(`${name} | Network response was not ok`);
            let data = await response.json();
            data = data.sort((a, b) => b.totalContributionAmount - a.totalContributionAmount);
            setCandidates(data);
        } catch (error) {
            console.error(`${name} | Error: `, error);
        };
    };
    useEffect(() => {
        if (year && chamber && state && district) fetchCandidates();
    }, [year, chamber, state, district]);
};