import React, { useEffect, useState } from "react";
import useFetchLegend from "../../../hooks/useFetchLegend";
import calculatePercentage from "../../../lib/calculatePercentage";
import formatCurrency from "../../../lib/formatCurrency";
import showStateName from "../../../lib/showStateName";
import styles from "../../../styles/candidate/Legend.module.css";
import {
    greenOpaque,
    greenTransparent,
    brownOpaque,
    brownTransparent
} from "../../../lib/colors";


function Renderer({ legend, state, amt }) {

    const [isMobile, setIsMobile] = useState(window.innerWidth < 768);
    useEffect(() => {
        const handleResize = () => {
            setIsMobile(window.innerWidth < 768);
        };
        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize", handleResize);
    }, []);

    const sortedItems = legend.sort((a, b) => {
        return a.LOCATION === "IN"
            ? 1
            : -1
    });
    return (
        <div className={styles.legendContainer}>
            {sortedItems.map((constituency, index) => (
                <div
                    className={styles.legendTitle}
                    key={index}
                    style={{
                        borderColor: `${
                            constituency.LOCATION === "IN"
                                ? greenOpaque
                                : brownOpaque
                        }`,
                        background: `${
                            constituency.LOCATION === "IN"
                                ? greenTransparent
                                : brownTransparent
                        }`,
                        color: `${
                            constituency.LOCATION === "IN"
                                ? "black"
                                : "black"
                        }`
                    }}
                >
                    <div>
                        {
                            constituency.LOCATION === "IN"
                                ? `From inside ${
                                    isMobile 
                                        ? state
                                        : showStateName(state)
                                }`
                                : `From outside ${
                                    isMobile
                                        ? state
                                        : showStateName(state)
                                }`
                        }
                    </div>
                    <div className={styles.legendNums}>
                        <div>
                            {formatCurrency(constituency.AMT)}
                        </div>
                        <div>
                            ({calculatePercentage(constituency.AMT, amt)}%)
                        </div>
                    </div>
                     
                </div>
            ))}
        </div>
    );
};


export default function Legend({ year, state, candidate }) {

    const { candId, amt } = candidate; 
    const [legend, setLegend] = useState([]);

    useFetchLegend(year, state, candId, setLegend);

    return (
        <Renderer
            legend={legend}
            state={state}
            amt={amt}
        />
    );

};
