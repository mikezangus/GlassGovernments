import React from "react";
import Bio from "./candidate/Bio";
import Legend from "./candidate/chart/Legend";
import Chart from "./candidate/chart/Chart";
import Map from "./candidate/map/Map";
import Cities from "./candidate/Cities";
import styles from "../styles/candidate/Candidate.module.css";


export default function Candidate({ year, state, district, candidate }) {

    return (

        <div className={styles.candidateContainer}>

            <div className={styles.box}>
    
                <Bio
                    state={state}
                    district={district}
                    candidate={candidate}
                />

                <Legend
                    year={year}
                    state={state}
                    candidate={candidate}
                />

                <Chart
                    year={year}
                    state={state}
                    candidate={candidate}
                />

                <Cities 
                    year={year}
                    candidate={candidate}
                />

                <Map
                    year={year}
                    state={state}
                    candidate={candidate}
                />

            </div>
    
        </div>
    
    );

};
