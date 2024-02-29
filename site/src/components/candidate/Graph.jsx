import React, { useState, useEffect, useRef } from "react";
import { Line } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, TimeScale, TimeSeriesScale } from "chart.js";
import "chartjs-adapter-moment";


ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, TimeScale, TimeSeriesScale);


function useFetchData(year, candID, setChartData) {
    useEffect(() => {
        if (year && candID) {
            const fetchData = async () => {
                try {
                    const params = new URLSearchParams({ year, candID })
                    const url = `/api/candidate/graph?${params.toString()}`;
                    const response = await fetch(url);
                    const data = await response.json();

                    const labels = data.map(item => new Date(item.YEAR, item.MONTH - 1).toISOString());
                    const amounts = data.map(item => item.AMT); // Assuming AMT is already a number

                    setChartData({
                        labels,
                        datasets: [{
                            label: "Donations ($)",
                            data: amounts,
                            borderColor: "rgb(75, 192, 192)",
                            tension: 0.1
                        }]
                    });

                } catch (err) {
                    console.error("dsafasdffda", err);
                };
            };
            fetchData();
        }
    }, [year, candID, setChartData]);
};


function Renderer({ chartData }) {
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
                    maxRotation: 0,
                    autoSkip: true
                }
            },
            y: {
                beginAtZero: true
            }
        },
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                mode: "index",
                intersect: false
            }
        },
        maintainAspectRatio: true,
        responsive: true
    };
    const chartRef = useRef();
    useEffect(() => {
        if (chartRef.current) {
            const chart = chartRef.current;
            const xScale = chart.scales['x'];
            const tickCount = xScale.ticks.length;
            const maxTicksToShow = 12;
            if (tickCount > maxTicksToShow) {
                const minTickToDisplay = tickCount - maxTicksToShow;
                xScale.options.ticks.min = xScale.ticks[minTickToDisplay];
                chart.update();
            }
        }
    }, [chartData]); 
    return (
        <div style={{ overflowX: "auto" }}>
            <Line
                ref={chartRef}
                data={chartData}
                options={options}
            />
        </div>
    );
};


export default function Graph({ year, candidate }) {

    const { candID } = candidate;

    const [chartData, setChartData] = useState({
        labels: [],
        datasets: [
            {
                label: "Donations ($)",
                data: [],
                borderColor: "rgb(75, 192, 192)",
                tension: 0.1
            }
        ]
    });

    useFetchData(year, candID, setChartData)


    return (
        <Renderer chartData={chartData} />
    );

};