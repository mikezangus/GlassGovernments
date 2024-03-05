import React, { useState } from "react";
import { Line } from "react-chartjs-2";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler,
    TimeScale,
    TimeSeriesScale
} from "chart.js";
import useFetchGraph from "../../hooks/useFetchGraph";
import "chartjs-adapter-moment";
import styles from "../../styles/Graph.module.css";


ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler,
    TimeScale,
    TimeSeriesScale
);


function CreateGraph({ data }) {

    const options = {
        scales: {
            x: {
                type: "time",
                time: {
                    unit: "month",
                    displayFormats: {
                        month: "MMM YYYY"
                    },
                    tooltipFormat: "MMM YYYY"
                },
                ticks: {
                    source: "labels",
                    autoSkip: false,
                    callback: function (value) {
                        const date = new Date(value);
                        const month = date.toLocaleString(
                            "default", { month: "short" }
                        );
                        const year = date.getFullYear();
                        return [month, year.toString()];
                    }
                },
            },
            y: {
                beginAtZero: true,
                stacked: true,
                display: true,
                position: "right",
            }
        },
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                mode: "index",
                intersect: true
            }
        },
        maintainAspectRatio: false,
        responsive: true
    };

    return (
        <div
            className={styles.graphContainer}
        >
            <Line
                data={data}
                options={options}
            />
        </div>
    );

};


function Renderer({ data }) {

    return (
        <div className={styles.container}>

            <CreateGraph data={data} />
        </div>
    );
}


export default function Graph({ year, state, candidate }) {

    const { candID } = candidate;

    const [data, setData] = useState({
        labels: [],
        datasets: []
    });
    useFetchGraph(year, state, candID, setData);

    console.log("Data via Graph function in Graph.jsx: ", data);

    if (!data.datasets || data.datasets.length === 0) {
        return null;
    }

    return (
        <Renderer data={data} />
    );

};
