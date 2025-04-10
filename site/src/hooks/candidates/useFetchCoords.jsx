import { useEffect, useState } from "react";


export default function useFetchCoords(year, candId, setCoords) {
    const name = "Fetch Coordinates Hook";
    const [loading, setLoading] = useState(false);
    const [skip, setSkip] = useState(0);
    const [isComplete, setIsComplete] = useState(false);
    const limit = 50000;
    useEffect(() => {
        if (!year || !candId || loading || isComplete) return;
        setLoading(true);
        const fetchCoords = async () => {
            try {
                const params = new URLSearchParams(
                    { year, candId, limit, skip }
                );
                const url = `/api/candidate/coords?${params.toString()}`;
                const response = await fetch(url);
                if (!response.ok) {
                    throw new Error(`
                        ${name} | Network response was not ok
                    `);
                }
                const data = await response.json();
                setCoords(prevCoords => [...prevCoords, ...data]);
                if (data.length < limit) {
                    setIsComplete(true);
                    setLoading(false);
                } else {
                    setSkip(prevSkip => prevSkip + limit);
                }
            } catch (error) {
                console.error(
                    `${name} | Error fetching data: ${error}`
                );
                setLoading(false);
            };
        };
        fetchCoords().finally(() => setLoading(false));
    }, [year, candId, skip, setCoords]);
    useEffect(() => {
        setSkip(0);
        setCoords([]);
        setIsComplete(false);
    }, [year, candId, setCoords]);
};
