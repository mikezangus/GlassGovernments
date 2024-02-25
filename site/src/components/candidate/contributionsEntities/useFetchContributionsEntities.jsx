import { useEffect } from "react";


export default function useFetchEntities(year, candID, setEntities) {
    const name = "Fetch Contributions Entities Hook"
    const fetchEntities = async () => {
        try {
            const params = new URLSearchParams(
                { year, candID }
            );
            const url = `/api/candidate/contributionsEntities?${params.toString()}`;
            const response = await fetch(url);
            if (!response.ok) throw new Error(`${name} | Network response was not ok`);
            const data = await response.json();
            const sortedData = data.sort(
                (a, b) => b.entityContAmt - a.entityContAmt
            );
            setEntities(sortedData);
        } catch (error) {
            console.error(`${name} | Error: `, error);
            setEntities([])
        };
    };
    useEffect(() => {
        if (year && candID) fetchEntities();
    }, [year, candID]);
};
