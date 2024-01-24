import { useEffect } from "react";


export default function useFetchStates(year, chamber, setStates) {
    const name = "Fetch States Hook";
    const fetchStates = async () => {
        try {
            const params = new URLSearchParams({ chamber });
            const url = `http://localhost:4000/api/states?${params.toString()}`;
            const response = await fetch(url);
            if (!response.ok) throw new Error(`${name} | Network response was not ok`);
            const data = await response.json();
            setStates(data);
        } catch (error) {
            console.error(`${name} | Error: `, error);
        };
    };
    useEffect(() => {
        if (year, chamber) fetchStates();
    }, [year, chamber]);
};