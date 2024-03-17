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


function PrintConstituency({ office, state, district }) {

    const [isMobile, setIsMobile] = useState(window.innerWidth < 820);
    useEffect(() => {
        const handleResize = () => {
            setIsMobile(window.innerWidth < 768);
        };
        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize", handleResize);
    }, []);

    let constituency;
    office === "S" || district == "00"
        ? isMobile
            ? constituency = state
            : constituency = showStateName(state)
        : constituency = `${state}-${district}`
    return constituency;
}


function Renderer({ legend, office, state, district, amt }) {

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
                            constituency.DOMESTIC
                                ? greenOpaque
                                : brownOpaque
                        }`,
                        background: `${
                            constituency.DOMESTIC
                                ? greenTransparent
                                : brownTransparent
                        }`,
                        color: `${
                            constituency.DOMESTIC
                                ? "black"
                                : "black"
                        }`
                    }}
                >
                    <div>
                        {
                            constituency.DOMESTIC
                                ? `From inside ${
                                    PrintConstituency({
                                        office,
                                        state,
                                        district
                                    })
                                }`
                                : `From outside ${
                                    PrintConstituency({
                                        office,
                                        state,
                                        district
                                    })
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
    console.log("candidate", candidate)
    const { office, district, candId, amt } = candidate; 
    const [legend, setLegend] = useState([]);

    useFetchLegend(year, state, candId, setLegend);

    return (
        <Renderer
            legend={legend}
            office={office}
            state={state}
            district={district}
            amt={amt}
        />
    );

};
