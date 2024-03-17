import { useEffect } from "react";
import {
    greenOpaque,
    greenTransparent,
    brownOpaque,
    brownTransparent
} from "../../lib/colors"


function WriteLabel({office, state, district}) {
    let label;
    office === "S" || district === "00"
        ? label = state
        : label = `${state}-${district}`
    return label;
};


export default function useFetchGraph(year, office, state, district, candID, setData) {

    const label = WriteLabel({ office, state, district });

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
                    const domesticData = data.map(
                        item => item.DOMESTIC_AMT
                    );
                    const foreignData = data.map(
                        item => item.FOREIGN_AMT
                    );

                    setData({
                        labels,
                        datasets: [
                            {
                                label: `Inside ${label}`,
                                data: domesticData,
                                borderColor: greenOpaque,
                                backgroundColor: greenTransparent,
                                fill: "origin",
                            },
                            {
                                label: `Outside ${label}`,
                                data: foreignData,
                                borderColor: brownOpaque,
                                backgroundColor: brownTransparent,
                                fill: "origin",
                            },
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
