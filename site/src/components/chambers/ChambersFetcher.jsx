import { useEffect } from "react";


export default function useFetchChambers(setChambers, setDefaultChamber, onChamberSelect) {
    useEffect(() => {
        const fetchChambers = async () => {
            try {
                const url = "http://localhost:4000/api/chambers";
                const response = await fetch(url);
                if (!response.ok) throw new Error("Chamber Fetcher | Network response was not ok");
                const data = await response.json();
                setChambers(data);
                if (data.length > 0) {
                    const defaultChamber = data[0];
                    setDefaultChamber(defaultChamber);
                    onChamberSelect(defaultChamber);
                };
            } catch (error) {
                console.error("Chamber Fetcher | Error fetching data: ", error);
            };
        };
        fetchChambers();
    }, []);
};