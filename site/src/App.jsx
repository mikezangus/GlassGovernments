import React, { useState } from "react";
import DropdownDistricts from "./components/DropdownDistricts";
import DropdownCandidates from "./components/DropdownCandidates";
import PanelCandidate from "./components/PanelCandidate";

export default function App() {

    const [selectedDistrict, setSelectedDistrict] = useState(null);
    const [selectedCandidate, setSelectedCandidate] = useState(null);

    const handleDistrictSelection = (district) => {
        setSelectedDistrict(district);
        setSelectedCandidate(null);
    };

    const handleCandidateSelection = (candidate) => {
        setSelectedCandidate(candidate);
    };

    return (
        <main>
            <div className="app-container" style={{ display: "flex" }}>
                <div className="left-container" style={{ width: "50%" }}>
                    <DropdownDistricts
                        onSelectedDistrict={handleDistrictSelection}
                        selectedDistrict={selectedDistrict}
                    />
                    {selectedDistrict && (
                        <DropdownCandidates
                            selectedDistrict={selectedDistrict}
                            onSelectedCandidate={handleCandidateSelection}
                            selectedCandidate={selectedCandidate}
                        />
                    )}
                </div>
                <PanelCandidate candidate={selectedCandidate} />
            </div>
        </main>
    );
};