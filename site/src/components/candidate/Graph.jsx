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

    const graphCanvasRef = useRef();
    const totalWidth = data.labels.length * 69;

    useEffect(() => {
        const element = graphCanvasRef.current;
        if (element) {

            // console.log("ELEMENT: ", element)
            // console.log("WIDTH BEFORE: ", element.style.width)

            graphCanvasRef.current.style.width = `${totalWidth}px`;

            // console.log("WIDTH AFTER: ", element.style.width);

            // console.log("SCROLL OUTSIDE TIMEOUT: ", element.scrollLeft);
            // setTimeout(() => {
            //     console.log("SCROLL INSIDE TIMEOUT: ", element.scrollLeft);
            //     console.log("element.scrollWidth: ", element.scrollWidth);
            //     console.log("element.clientWidth: ", element.clientWidth)
            //     const maxScrollLeft = element.scrollWidth - element.clientWidth;
            //     console.log("maxScrollLeft: ", maxScrollLeft);
            //     element.scrollLeft = 1000;
            //     console.log("SCROLL AFTER ASSIGNMENT: ", element.scrollLeft);
            // }, 10000)
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
        <div className={styles.graphContainer}>
            <div className={styles.graphCanvas} ref={graphCanvasRef}>
                <Line
                    data={data}
                    options={options}
                />
            </div>
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

    if (!data.datasets || data.labels.length === 0) {
        return null;
    }

    return (
        <Renderer data={data} />
    );

};
