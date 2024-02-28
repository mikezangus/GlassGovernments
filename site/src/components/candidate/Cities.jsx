import React, { useState } from "react";
import useFetchCities from "../../hooks/useFetchCities";
import formatCurrency from "../../lib/formatCurrency";


function Renderer({ locations }) {

    return (
        <>
            <ul>
                {locations.map((location, index) => (
                    <li key={index}>
                        {location.CITY} - {formatCurrency(location.AMT)} - {location.COUNT}
                    </li>
                ))}
            </ul>
        </>
    );
};


export default function Cities({ year, candidate }) {

    const { candID } = candidate;

    const [locations, setLocations] = useState([]);

    useFetchCities(year, candID, setLocations);

    return (
        <Renderer locations={locations}/>
    );

};