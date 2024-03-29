import { useEffect } from "react";


export default function useFetchDistricts(year, office, state, setDistricts) {
    const name = "Fetch Districts Hook";
    useEffect(() => {
        if (year && office && state) {
            const fetchDistricts = async () => {
                try {
                    const params = new URLSearchParams({ year, office, state });
                    const url = `/api/selections/districts?${params.toString()}`;
                    const response = await fetch(url);
                    if (!response.ok) throw new Error(`${name} | Network response was not ok`);
                    const data = await response.json();
                    setDistricts(data);
                } catch (error) {
                    console.error(`${name} | Error: `, error);
                };
            };
            fetchDistricts();
        };
    }, [year, office, state]);
};
