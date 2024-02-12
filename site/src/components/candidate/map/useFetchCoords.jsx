import { useEffect } from "react";


export default function useFetchCoords(year, candID, setCoords) {
    const name = "Fetch Coordinates Hook"
    const fetchCoords = async () => {
        try {
            const params = new URLSearchParams(
                { year, candID }
            );
            const url = `http://localhost:4000/api/candidate/coords?${params.toString()}`;
            const response = await fetch(url);
            if (!response.ok) throw new Error(`${name} | Network response was not ok`);
            const data = await response.json();
            console.log("DATA:", data)
            setCoords(data);
        } catch (error) {
            console.error(`${name} | Error fetching data: ${error}`);
            setCoords([]);
        };
    };
    useEffect(() => {
        if (year && candID) fetchCoords();
    }, [year, candID]);
};