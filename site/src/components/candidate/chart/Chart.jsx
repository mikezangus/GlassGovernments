import React, { useState } from "react";
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
import ChartData from "./ChartData";
import ChartYAxis from "./ChartYAxis";
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


export default function Chart({ year, state, candidate }) {

    const { office, district, candId } = candidate;

    const [data, setData] = useState({
        labels: [],
        datasets: []
    });
    useFetchGraph(year, office, state, district, candId, setData);

    if (!data.datasets || data.labels.length === 0) {
        return null;
    }

    const sums = data.labels.map((_, idx) => (
        data.datasets.reduce((sum, dataset) => (
            sum + (dataset.data[idx] || 0)
        ), 0)
    ));
    const maxSum = Math.max(...sums);
    const digitCount = maxSum.toString().length;

    return (
        <div className={styles.mainContainer}>
            <ChartYAxis
                inputData={data}
                maxSum={maxSum}
            />
            <ChartData
                data={data}
                digitCount={digitCount}
            />
        </div>
    );

};
