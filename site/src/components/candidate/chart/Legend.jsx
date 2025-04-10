import React, { useEffect, useState } from "react";
import useFetchLegend from "../../../hooks/candidates/useFetchLegend";
import calculatePercentage from "../../../lib/calculatePercentage";
import formatCurrency from "../../../lib/formatCurrency";
import showStateName from "../../../lib/showStateName";
import {
    greenOpaque,
    greenTransparent,
    brownOpaque,
    brownTransparent
} from "../../../lib/colors";
import useIsMobile from "../../../lib/useIsMobile";
import styles from "../../../styles/candidate/Legend.module.css";



function PrintConstituency({ office, state, district }) {

    let constituency;
    const isMobile = useIsMobile();
    office === "S" || district == "00"
        ? isMobile
            ? constituency = state
            : constituency = showStateName(state)
        : constituency = `${state}-${district}`
    return constituency;
}


function Renderer({ legend, office, state, district, amt }) {

    const sortedItems = legend.sort((a, b) => {
        if (a.DOMESTIC === b.DOMESTIC) {
            return 0;
        }
        return a.DOMESTIC ? 1 : -1;
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
