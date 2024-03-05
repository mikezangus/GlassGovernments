import { useEffect } from "react";


export default function useFetchConstituencies(year, state, candID, setConstituencies) {
    const name = "Fetch Constituencies Hook";
    useEffect(() => {
        const fetchConstituencies = async () => {
            try {
                const params = new URLSearchParams(
                    { year, state, candID }
                );
                const url = `/api/candidate/constituency?${params.toString()}`;
                const response = await fetch(url);
                if (!response.ok) {
                    throw new Error(
                        name, " | Network response was not ok"
                    );
                }
                let data = await response.json();
                console.log("DATA: ", data)
                setConstituencies(data);
            } catch (err) {
                console.error(name, " | Error: ", err);
            };
        };
        fetchConstituencies(year, state, candID, setConstituencies);
    }, [year, state, candID, setConstituencies]);
};
