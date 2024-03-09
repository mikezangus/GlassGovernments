import React, { useEffect, useMemo, useRef, useState } from "react";
import { Line } from "react-chartjs-2";
import styles from "../../../styles/candidate/Chart.module.css";


function getPadding(digitCount) {
    switch(digitCount) {
        case 3: return 18;
        case 4: return 27;
        case 5: return 34;
        case 6: return 41;
        case 7: return 51;
        default: return 0;
    }
};


const useResize = () => {
    const [isMobile, setIsMobile] = useState(window.innerWidth < 820);
    useEffect(() => {
        const handleResize = () => setIsMobile(window.innerWidth < 820);
        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize", handleResize);
    }, []);
    return isMobile;
};


function formatTick(value) {
    const date = new Date(value);
    const month = date.toLocaleString(
        "default",
        { month: "short" }
    );
    const year = date.getFullYear();
    return [month, year.toString()];
};


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
                callback: (value) => formatTick(value)
            },
        },
        y: {
            beginAtZero: true,
            stacked: true,
            display: true,
            position: "right",
            grid: {
                drawBorder: true,
                drawOnChartArea: true
            },
            ticks: {
                display: false,
                autoSkip: false
            }
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


export default function ChartData({ data, digitCount }) {

    const isMobile = useResize();

    const padding = getPadding(digitCount);

    const chartContainerRef = useRef(null);
    const chartContainerWidth = useMemo(() => {
        return chartContainerRef.current?.offsetWidth || 0;
    }, [chartContainerRef.current?.offsetWidth]);

    const labelCount = data.labels.length;
    const labelSpacing = isMobile ? 75: 100;
    let chartWidth = labelCount * labelSpacing;
    if (chartWidth < chartContainerWidth) {
        chartWidth = chartContainerWidth - padding
    }

    const chartScrollContainerRef = useRef();
    useEffect(() => {
        const element = chartScrollContainerRef.current;
        if (element) {
            element.style.width = `${chartWidth + padding}px`;
            element.scrollLeft = chartWidth;
        }
    }, [data.labels.length, chartWidth]);

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
                    style={{
                        width: chartWidth,
                        paddingRight: padding
                    }}
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

