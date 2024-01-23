import React from "react";
import ShowChambers from "./chambers/ShowChambers.jsx";
import ShowStates from "./states/ShowStates.jsx";
import ShowDistricts from "./districts/ShowDistricts.jsx";
import ShowCandidates from "./candidates/ShowCandidates.jsx";
import useCountDistricts from "./districts/useCountDistricts.jsx";
import "../../css/index.css";


export default function RenderSelections(
    {
        handleChamberSelection, selectedChamber,
        handleStateSelection, selectedState,
        handleDistrictSelection, selectedDistrict,
        handleCandidateSelection
    }
) {

    const districtCount = useCountDistricts(selectedChamber, selectedState, handleDistrictSelection);

    return (

        <div className="left">

            <ShowChambers
                onChamberSelect={handleChamberSelection}
            />

            {selectedChamber && (
                <ShowStates
                    chamber={selectedChamber}
                    onStateSelect={handleStateSelection}
                />
            )}

            {selectedChamber === "HOUSE" && selectedState && districtCount > 1 && (
                <ShowDistricts
                    chamber={selectedChamber}
                    state={selectedState}
                    onDistrictSelect={handleDistrictSelection}
                />
            )}

            {selectedChamber && selectedState && selectedDistrict && (
                <ShowCandidates
                    chamber={selectedChamber}
                    state={selectedState}
                    district={selectedDistrict}
                    onCandidateSelect={handleCandidateSelection}
                />
            )}

        </div>
    );

};