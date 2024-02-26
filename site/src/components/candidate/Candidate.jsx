import React from "react";
import Bio from "./bio/Bio";
import ContributionsTotal from "./contributionsTotal/ContributionsTotal";
import ContributionsEntities from "./contributionsEntities/ContributionsEntities";
import Map from "./map/Map";
import styles from "../../styles/Candidate.module.css"


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
