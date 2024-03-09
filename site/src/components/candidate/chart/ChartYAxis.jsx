import React from "react";
import { Line } from "react-chartjs-2";
import styles from "../../../styles/candidate/Chart.module.css";


export default function ChartYAxis({ inputData, maxSum }) {

    const data = {
        labels: inputData.labels,
        datasets: [{
            data: new Array(
                inputData.labels.length
            ).fill(null)
        }]
    };

    const options = {
        scales: {
            x: {
                display: false
            },
            y: {
                beginAtZero: true,
                stacked: true,
                display: true,
                suggestedMax: maxSum,
                position: "right",
                grid: {
                    drawBorder: false,
                    drawOnChartArea: false,
                },
            }
        },
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                enabled: false
            }
        },
        maintainAspectRatio: false,
        responsive: true
    };

    return (
        <div className={styles.yAxisContainer}>
            <Line
                data={data}
                options={options}
            />
        </div>
    );

};
