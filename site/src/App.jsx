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
        <div>
            <DropdownDistricts onSelectedDistrict={handleDistrictSelection} />
            {selectedDistrict && (
                <DropdownCandidates
                    selectedDistrict={selectedDistrict}
                    onSelectedCandidate={handleCandidateSelection}
                />
            )}
            {selectedCandidate && <PanelCandidate candidate={selectedCandidate} />}
        </div>
    );
};