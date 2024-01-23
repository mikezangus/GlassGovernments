import React from "react";
import ShowBio from "./bio/ShowBio";
import ShowContributionsTotal from "./contributionsTotal/ShowContributionsTotal";
import ShowContributionsEntities from "./contributionsEntities/ShowContributionsEntities";
import ShowMap from "./map/ShowMap";
import "../../css/candidate.css"


export default function RenderCandidate({ chamber, state, district, candidate }) {

    return (

        <div className="right">
    
            <ShowBio
                chamber={chamber}
                state={state}
                district={district}
                candidate={candidate}
            />

            <ShowContributionsTotal
                chamber={chamber}
                state={state}
                district={district}
                candidate={candidate}
            />
        
            <ShowContributionsEntities
                chamber={chamber}
                state={state}
                district={district}
                candidate={candidate}
            />
        
            <ShowMap
                chamber={chamber}
                state={state}
                district={district}
                candidate={candidate}
            />
    
        </div>
    
    );

};