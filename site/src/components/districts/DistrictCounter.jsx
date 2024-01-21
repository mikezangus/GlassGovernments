import { useState, useEffect } from "react";


export default function useCountDistricts(chamber, state, handleDistrictSelection) {
    const [districtCount, setDistrictCount] = useState(0);
    useEffect(() => {
        const countDistricts = async () => {
            try {
                const params = new URLSearchParams({ chamber, state });
                const url = `http://localhost:4000/api/districts?${params.toString()}`;
                const response = await fetch(url);
                if (!response.ok) throw new Error("District Counter | Network response was not ok");
                const data = await response.json();
                if (data.length === 1) { handleDistrictSelection(data[0]) };
                setDistrictCount(data.length);
            } catch (error) {
                console.error("District Counter | Error: ", error);
                setDistrictCount(0);
            };
        };
        if (chamber && state) {
            countDistricts();
        }
    }, [chamber, state]);
    return districtCount;
};