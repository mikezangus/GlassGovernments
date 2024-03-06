import React, { useEffect, useState } from "react";
import useFetchConstituencies from "../../hooks/useFetchConstituencies";
import calculatePercentage from "../../lib/calculatePercentage";
import formatCurrency from "../../lib/formatCurrency";
import showStateName from "../../lib/showStateName";
import styles from "../../styles/Candidate.module.css";
import {
    greenOpaque,
    greenTransparent,
    brownOpaque,
    brownTransparent
} from "../../lib/colors";


function Renderer({ constituencies, state, totalContAmt }) {

    const [isMobile, setIsMobile] = useState(window.innerWidth < 768);
    useEffect(() => {
        const handleResize = () => {
            setIsMobile(window.innerWidth < 768);
        };
        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize", handleResize);
    }, []);

    const sortedItems = constituencies.sort((a, b) => {
        return a.LOCATION === "IN"
            ? 1
            : -1
    });
    return (
        <div className={styles.constituencies}>
            {sortedItems.map((constituency, index) => (
                <div
                    className={styles.legend}
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
                    <div className={styles.amounts}>
                        <div>
                            {formatCurrency(constituency.AMT)}
                        </div>
                        <div>
                            ({calculatePercentage(constituency.AMT, totalContAmt)}%)
                        </div>
                    </div>
                     
                </div>
            ))}
        </div>
    );
};


export default function Constituencies({ year, state, candidate }) {

    const { candID, totalContAmt } = candidate;

    const [constituencies, setConstituencies] = useState([]);

    useFetchConstituencies(year, state, candID, setConstituencies);

    return (
        <Renderer
            constituencies={constituencies}
            state={state}
            totalContAmt={totalContAmt}
        />
    );

};
