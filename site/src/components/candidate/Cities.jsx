import React, { useState } from "react";
import useFetchCities from "../../hooks/useFetchCities";
import formatCurrency from "../../lib/formatCurrency";
import capitalizeWord from "../../lib/capitalizeWord";
import styles from "../../styles/candidate/Cities.module.css"


function Renderer({ locations }) {

    return (
        <div className={styles.citiesContainer}>
            <div className={styles.citiesTitle}>
                Top Cities
            </div>
  
            <ol className={styles.citiesList}>
                {locations.map((location, index) => (
                    <li
                        className={styles.citiesListItem}
                        key={index}
                    >
                        {capitalizeWord(location.CITY)}, {location.STATE}: {formatCurrency(location.AMT)}
                    </li>
                ))}
            </ol>
        </div>
    );
};


export default function Cities({ year, candidate }) {

    const { candId } = candidate;

    const [locations, setLocations] = useState([]);

    useFetchCities(year, candId, setLocations);

    console.log("locations", locations)

    return (
        <Renderer locations={locations}/>
    );

};
