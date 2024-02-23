import { useEffect } from "react";


export default function useFetchStates(year, office, setStates) {
    const name = "Fetch States Hook";
    const fetchStates = async () => {
        try {
            const params = new URLSearchParams({ year, office });
            const url = `/api/selections/states?${params.toString()}`;
            const response = await fetch(url);
            if (!response.ok) throw new Error(`${name} | Network response was not ok`);
            const data = await response.json();
            setStates(data);
        } catch (error) {
            console.error(`${name} | Error: `, error);
        };
    };
    useEffect(() => {
        if (year, office) fetchStates();
    }, [year, office]);
};
