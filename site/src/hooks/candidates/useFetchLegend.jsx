import { useEffect } from "react";


export default function useFetchLegend(year, state, candId, setConstituencies) {
    const name = "Fetch Legend Hook";
    useEffect(() => {
        const fetchConstituencies = async () => {
            try {
                const params = new URLSearchParams(
                    { year, state, candId }
                );
                const url = `/api/candidate/legend?${params.toString()}`;
                const response = await fetch(url);
                if (!response.ok) {
                    throw new Error(
                        name, " | Network response was not ok"
                    );
                }
                let data = await response.json();
                setConstituencies(data);
            } catch (err) {
                console.error(name, " | Error: ", err);
            };
        };
        fetchConstituencies(year, state, candId, setConstituencies);
    }, [year, state, candId, setConstituencies]);
};
