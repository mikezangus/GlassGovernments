import React from "react";
import ShowBio from "./bio/ShowBio";
import ShowContributionsTotal from "./contributionsTotal/ShowContributionsTotal";
import ShowContributionsEntities from "./contributionsEntities/ShowContributionsEntities";
import ShowMap from "./map/ShowMap";
import "../../css/candidate.css"


export default function RenderCandidate({ year, office, state, district, candidate }) {

    return (

        <div className="candidate">
    
            <ShowBio
                state={state}
                district={district}
                candidate={candidate}
            />

            <ShowContributionsTotal
                candidate={candidate}
            />

        
            <ShowContributionsEntities
                year={year}
                candidate={candidate}
            />

        
            {/* <ShowMap
                office={office}
                state={state}
                district={district}
                candidate={candidate}
            /> */}
    
        </div>
    
    );

};