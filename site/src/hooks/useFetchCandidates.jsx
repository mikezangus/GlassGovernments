import { useEffect } from "react";


export default function useFetchCandidates(year, office, state, district, setCandidates) {
    const name = "Fetch Candidates Hook";

    useEffect(() => {
        if (year && office && state && district) {
            const fetchCandidates = async () => {
                try {
                    const params = new URLSearchParams( { year, office, state, district });
                    const url = `/api/selections/candidates?${params.toString()}`;
                    const response = await fetch(url);
                    if (!response.ok) throw new Error(`${name} | Network response was not ok`);
                    let data = await response.json();
                    data = data.sort(
                        (a, b) => b.totalContAmt - a.totalContAmt
                    );
                    setCandidates(data);
                } catch (error) {
                    console.error(`${name} | Error: `, error);
                };
            };
            fetchCandidates();
        };
    }, [year, office, state, district]);
};
