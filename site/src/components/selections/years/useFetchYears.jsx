import { useEffect } from "react";


export default function useFetchYears(setYears, setDefaultYear, onYearSelect) {
    const name = "Years Hook";
    const fetchYears = async () => {
        try {
            const url = "/api/selections/years";
            console.log("URL: ", url)
            const response = await fetch(url);
            console.log("RESPONSE: ", response);
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
