import { useEffect } from "react";


export default function useFetchCities(year, candID, setCities) {
    const name = "Fetch Cities Hook";
    const fetchCities = async () => {
        try {
            const params = new URLSearchParams(
                { year, candID }
            );
            const url = `/api/candidate/cities?${params.toString()}`;
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(name, " | Network response was not ok")
            }
            let data = await response.json();
            // data = data
            //     .filter(item => item != null)
            //     .sort((a, b) => b - a);
            console.log("CITIES", data)
            setCities(data);
        } catch (err) {
            console.error(name, " | Error: ", err);
        };
    };
    useEffect(() => { fetchCities() }, []);
};
