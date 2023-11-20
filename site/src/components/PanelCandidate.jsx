import React from "react";
import "./PanelCandidate.css";

export default function PanelCandidate ( {candidate} ) {
    return (
        <div className={`panel-candidate ${candidate ? "white-background" : ""}`}>
            {candidate && (
                <div className="candidate-info">
                    {candidate._id.lastName}
                </div>
            )}
        </div>
    );
};