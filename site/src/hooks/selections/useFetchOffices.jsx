import { useEffect } from "react";


export default function useFetchOffices(year, setOffices, setDefaultOffice, onOfficeSelect) {
    const name = "Fetch Offices Hook";
    useEffect(() => {
        if (year) {
            const fetchOffices = async () => {
                try {
                    const params = new URLSearchParams({ year })
                    const url = `/api/selections/offices?${params.toString()}`;
                    const response = await fetch(url);
                    if (!response.ok) throw new Error(`${name} | Network response was not ok`);
                    const data = await response.json();
                    if (data.length > 0) {
                        const defaultOffice = data[0];
                        setDefaultOffice(defaultOffice);
                        onOfficeSelect(defaultOffice);
                    }
                    setOffices(data);
                } catch (error) {
                    console.error(`${name} | Error: `, error);
                };
            };
            fetchOffices();
        };
    }, [year]);
};
