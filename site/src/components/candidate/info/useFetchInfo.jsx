import { useEffect } from "react";


export default function useFetchInfo(chamber, state, district, candidate) {
    useEffect(() => {
        const fetchInfo = async () => {
            try {
                const { _id: { firstName, lastName, party } } = candidate;
                const params = new URLSearchParams(
                    { chamber, state, district, firstName, lastName, party }
                );
                const url = `http://localhost:4000/api/candidate/info?${params.toString()}`;
                const response = await fetch(url);
                if (!response.ok) throw new Error("Candidate Info Fetcher | Network response was not ok");
                const data = await response.json();
                return data
            } catch (error) {
                console.error("Candidate Info Fetcher | Error fetching data: ", error);
            };
        };
        if (chamber && state && district && candidate) {
            fetchInfo();
        };
    }, [chamber, state, district, candidate]);
};