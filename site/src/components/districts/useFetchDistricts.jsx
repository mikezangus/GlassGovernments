import { useEffect } from "react";


export default function useFetchDistricts(chamber, state, setDistricts) {
    const name = "Fetch Districts Hook";
    const fetchDistricts = async () => {
        try {
            const params = new URLSearchParams({ chamber, state });
            const url = `http://localhost:4000/api/districts?${params.toString()}`;
            const response = await fetch(url);
            if (!response.ok) throw new Error(`${name} | Network response was not ok`);
            const data = await response.json();
            setDistricts(data);
        } catch (error) {
            console.error(`${name} | Error: `, error);
        };
    };
    useEffect(() => {
        if (chamber && state) fetchDistricts();
    }, [chamber, state]);
};