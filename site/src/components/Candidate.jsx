import React from "react";
import Bio from "./candidate/bio/Bio";
import ContributionsTotal from "./candidate/contributionsTotal/ContributionsTotal";
import Map from "./candidate/map/Map";
import Constituencies from "./candidate/Constituencies";
import Graph from "./candidate/Graph";
import styles from "../styles/Candidate.module.css";


export default function Candidate({ year, state, district, candidate }) {

    return (

        <div className={styles.candidateContainer}>

            <div className={styles.candidateInfo}>
    
                <Bio
                    state={state}
                    district={district}
                    candidate={candidate}
                />

                <ContributionsTotal
                    candidate={candidate}
                />

                <Constituencies
                    year={year}
                    state={state}
                    candidate={candidate}
                />

                <Graph
                    year={year}
                    state={state}
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
