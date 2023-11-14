import React from "react";
import "./PanelCandidate.css";

export default function PanelCandidate ( {selectedCandidate} ) {
    if (!selectedCandidate) {
        return null;
    }
    return (
        <div className="panel">
            {selectedCandidate.candidate_first_name} {selectedCandidate.candidate_last_name}
            <div>State: {selectedCandidate.candidate_state}</div>
            <div>District: {selectedCandidate.candidate_district}</div>
        </div>
    );
}