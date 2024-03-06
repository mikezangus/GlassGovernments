import { useEffect } from "react";


export default function useFetchCities(year, candId, setCities) {
    const name = "Fetch Cities Hook";
    useEffect(() => {
        const fetchCities = async () => {
            try {
                const params = new URLSearchParams(
                    { year, candId }
                );
                const url = `/api/candidate/cities?${params.toString()}`;
                const response = await fetch(url);
                if (!response.ok) {
                    throw new Error(
                        name, " | Network response was not ok"
                    );
                }
                let data = await response.json();
                data = data
                    .filter(item => item != null)
                    .sort((a, b) => b - a);
                setCities(data);
            } catch (err) {
                console.error(name, " | Error: ", err);
            };
        };
        fetchCities();
    }, [year, candId, setCities]);
};
