import { useEffect } from "react";


export default function useFetchYears(setYears, setDefaultYear, onYearSelect) {
    const name = "Fetch Years Hook";
    const fetchYears = async () => {
        try {
            let data = ["2020", "2022", "2024"];
            data = data.sort((a, b) => b - a);
            setYears(data);
            const defaultYear = data[0];
            setDefaultYear(defaultYear);
            onYearSelect(defaultYear);
        } catch (error) {
            console.error(`${name} | Error: `, error);
        };
    };
    useEffect(() => { fetchYears() }, []);
};