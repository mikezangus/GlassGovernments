import { useEffect } from "react";


export default function useFetchGraph(year, state, candID, setData) {
    useEffect(() => {
        if (year && candID) {
            const fetchGraph = async () => {
                try {
                    const params = new URLSearchParams({ year, state, candID })
                    const url = `/api/candidate/graph?${params.toString()}`;
                    const response = await fetch(url);
                    if (!response.ok) {
                        throw new Error("NETWORK RESPONSE WAS NOT OK")
                    }
                    const data = await response.json();

                    const labels = data.map(
                        item => new Date(
                            item.YEAR, item.MONTH - 1
                        ).toISOString()
                    );
                    const inStateData = data.map(
                        item => item.INSIDE_AMT
                    );
                    const outStateData = data.map(
                        item => item.OUTSIDE_AMT
                    );

                    setData({
                        labels,
                        datasets: [
                            {
                                label: `Inside ${state}`,
                                data: inStateData,
                                borderColor: "rgb(54, 162, 235)",
                                backgroundColor: "rgba(54, 162, 235, 0.5)",
                                fill: "origin",
                            },
                            {
                                label: `Outside ${state}`,
                                data: outStateData,
                                borderColor: "rgb(255, 99, 132)",
                                backgroundColor: "rgba(255, 99, 132, 0.5)",
                                fill: "origin",
                            }
                        ]
                    });

                } catch (err) {
                    console.error("Use Fetch Graph | ", err);
                };
            };
            fetchGraph();
        }
    }, [year, state, candID, setData]);
};
