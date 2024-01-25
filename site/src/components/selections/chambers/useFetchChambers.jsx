import { useEffect } from "react";


export default function useFetchChambers(year, setChambers, setDefaultChamber, onChamberSelect) {
    const name = "Fetch Chambers Hook";
    const fetchChambers = async () => {
        try {
            const url = "http://localhost:4000/api/chambers";
            const response = await fetch(url);
            if (!response.ok) throw new Error(`${name} | Network response was not ok`);
            const data = await response.json();
            if (data.length > 0) {
                const defaultChamber = data[0];
                setDefaultChamber(defaultChamber);
                onChamberSelect(defaultChamber);
            }
            setChambers(data);
        } catch (error) {
            console.error(`${name} | Error: `, error);
        };
    };
    useEffect(() => {
        if (year) fetchChambers();
    }, [year]);

};