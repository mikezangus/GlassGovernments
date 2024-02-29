import { useEffect } from "react";


export default function useFetchCoords(year, candID, setCoords) {
    const name = "Fetch Coordinates Hook"
    useEffect(() => {
        if (year && candID) {
            const fetchCoords = async () => {
                try {
                    const params = new URLSearchParams(
                        { year, candID }
                    );
                    const url = `/api/candidate/coords?${params.toString()}`;
                    const response = await fetch(url);
                    if (!response.ok) throw new Error(`${name} | Network response was not ok`);
                    const data = await response.json();
                    setCoords(data);
                } catch (error) {
                    console.error(`${name} | Error fetching data: ${error}`);
                    setCoords([]);
                };
            };
            fetchCoords();
        };
    }, [year, candID]);
};
