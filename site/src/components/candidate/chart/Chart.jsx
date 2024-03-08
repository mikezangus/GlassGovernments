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
import useFetchGraph from "../../../hooks/useFetchGraph";
import styles from "../../../styles/candidate/Chart.module.css";


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


function CreateChart({ data }) {

    const [isMobile, setIsMobile] = useState(window.innerWidth < 768);
    useEffect(() => {
        const handleResize = () => {
            setIsMobile(window.innerWidth < 768);
        };
        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize", handleResize);
    }, []);

    let labelSpacing
    isMobile ? labelSpacing = 75 : labelSpacing = 100

    const chartContainerRef = useRef(null);
    const [chartContainerWidth, setChartContainerWidth] = useState(0);
    useEffect(() => {
        const updateChartContainerWidth = () => {
            if (chartContainerRef.current) {
                setChartContainerWidth(chartContainerRef.current.offsetWidth)
            }
        };
        updateChartContainerWidth();
        window.addEventListener("resize", updateChartContainerWidth);
        return () => window.removeEventListener("resize", updateChartContainerWidth)
    }, []);

    const labelCount = data.labels.length;
    let chartWidth = labelCount * labelSpacing;
    if (chartWidth < chartContainerWidth) {
        chartWidth = chartContainerWidth
    }

    const chartScrollContainerRef = useRef();
    useEffect(() => {
        const element = chartScrollContainerRef.current;
        if (element) {
            element.style.width = `${chartWidth}px`;
            element.scrollLeft = chartWidth;
        }
    }, [data.labels.length, chartWidth]);

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
        <div
            className={styles.chartContainer}
            ref={chartContainerRef}
        >
            <div
                className={styles.chartScrollContainer}
                ref={chartScrollContainerRef}
            >
                <div
                    className={styles.chartCanvas}
                    style={{ width: chartWidth }}
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



export default function Chart({ year, state, candidate }) {

    const { candId } = candidate;

    const [data, setData] = useState({
        labels: [],
        datasets: []
    });
    useFetchGraph(year, state, candId, setData);

    if (!data.datasets || data.labels.length === 0) {
        return null;
    }

    return (
        <CreateChart data={data} />
    );

};
