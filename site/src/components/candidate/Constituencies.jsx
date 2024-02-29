import React, { useState } from "react";
import useFetchConstituencies from "../../hooks/useFetchConstituencies";
import calculatePercentage from "../../lib/calculatePercentage";
import formatCurrency from "../../lib/formatCurrency";
import showStateName from "../../lib/showStateName";


function Renderer({ constituencies, state, totalContAmt }) {

    const handlestuff = (constituency, state) => {
        let txt
        if (constituency.LOCATION === "IN") {
            txt = `From inside of ${showStateName(state)}`;
        }
        else if (constituency.LOCATION === "OUT") {
            txt = `From outside of ${showStateName(state)}`;
        }
        return txt
    };

    return (
        <>
            {constituencies.map((constituency, index) => (
                <div key={index}>
                    {handlestuff(constituency, state)}: {formatCurrency(constituency.AMT)} ({calculatePercentage(constituency.AMT, totalContAmt)}% of total)
                </div>
            ))}
        </>
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
