import React, { useEffect, useRef, useState } from "react";
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
import "chartjs-adapter-moment";
import useFetchGraph from "../../hooks/useFetchGraph";
import styles from "../../styles/candidate/Graph.module.css";



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

    const graphContainerRef = useRef();
    const totalWidth = data.labels.length * 69;

    useEffect(() => {
        const element = graphContainerRef.current;
        if (element) {
            element.style.width = `${totalWidth}px`;
            element.scrollLeft = totalWidth;
        }
    }, [data.labels.length, totalWidth]);

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
                    },
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
        responsive: true,

    };

    return (
        <div className={styles.mainContainer}>
            <div
                className={styles.graphContainer}
                ref={graphContainerRef}
            >
                <div
                    className={styles.canvas}
                    style={{ width: `${totalWidth}px` }}
                >
                    <Line
                        data={data}
                        options={options}
                    />
                </div>
            </div>
        </div>

    );

};



export default function Graph({ year, state, candidate }) {

    const { candID } = candidate;

    const [data, setData] = useState({
        labels: [],
        datasets: []
    });
    useFetchGraph(year, state, candID, setData);

    if (!data.datasets || data.labels.length === 0) {
        return null;
    }

    return (
        <CreateGraph data={data} />
    );

};
