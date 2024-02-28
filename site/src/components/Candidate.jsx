import React from "react";
import Bio from "./candidate/bio/Bio";
import ContributionsTotal from "./candidate/contributionsTotal/ContributionsTotal";
import Cities from "./candidate/Cities"
import Map from "./candidate/map/Map";
import styles from "../styles/Candidate.module.css";


export default function Candidate({ year, state, district, candidate }) {

    return (

        <div className={styles.candidate}>
    
            <Bio
                state={state}
                district={district}
                candidate={candidate}
            />

            <ContributionsTotal
                candidate={candidate}
            />

            <Cities
                year={year}
                candidate={candidate}
            />

        
            {/* <ContributionsEntities
                year={year}
                candidate={candidate}
            /> */}

            <Map
                year={year}
                candidate={candidate}
            />
    
        </div>
    
    );

};
