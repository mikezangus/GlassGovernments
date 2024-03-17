import { useState, useEffect } from "react";


export default function useFetchDistrictCount(year, office, state, handleDistrictSelection) {

    const name = "Count Districts Hook";
    const [districtCount, setDistrictCount] = useState(0);

    useEffect(() => {
        if (year && office && state) {
            const fetchDistrictCount = async () => {
                try {
                    const params = new URLSearchParams({ year, office, state });
                    const url = `/api/selections/districts?${params.toString()}`;
                    const response = await fetch(url);
                    if (!response.ok) throw new Error(`${name} | Network response was not ok`);
                    const data = await response.json();
                    if (data.length === 1) handleDistrictSelection(data[0]);
                    setDistrictCount(data.length);
                } catch (error) {
                    console.error(`${name} | Error: `, error);
                    setDistrictCount(0);
                };
            };
            fetchDistrictCount();
        };
    }, [year, office, state]);
    return districtCount;
};
