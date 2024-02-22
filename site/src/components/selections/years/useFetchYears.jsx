import { useEffect } from "react";


export default function useFetchYears(setYears, setDefaultYear, onYearSelect) {
    const name = "Fetch Years Hook";
    const fetchYears = async () => {
        try {
            const url = "http://localhost:4000/api/years";
            const response = await fetch(url);
            if (!response.ok) throw new Error(`${name} | Network response was not ok`);
            let data = await response.json();
            data = data.filter(item => item != null);
            data = data.sort((a, b) => b - a);
            if (data.length > 0) {
                const defaultYear = data[0];
                setDefaultYear(defaultYear);
                onYearSelect(defaultYear);
            }
            setYears(data);
        } catch (error) {
            console.error(`${name} | Error: `, error);
        };
    };
    useEffect(() => { fetchYears() }, []);
};
