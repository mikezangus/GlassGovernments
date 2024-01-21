import { useEffect } from "react";


export default function useFetchStates(chamber, setStates) {
    useEffect(() => {
        const fetchStates = async () => {
            try {
                const params = new URLSearchParams(
                    { chamber }
                );
                const url = `http://localhost:4000/api/states?${params.toString()}`;
                const response = await fetch(url);
                if (!response.ok) throw new Error("State Fetcher | Network response was not ok");
                const data = await response.json();
                setStates(data);
            } catch (error) {
                console.error("State Fetcher | Error fetching data: ", error);
            };
        };
        if (chamber) {
            fetchStates();
        };
    }, [chamber]);
};