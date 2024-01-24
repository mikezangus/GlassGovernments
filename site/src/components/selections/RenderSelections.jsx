import React from "react";
import ShowYears from "./years/ShowYears.jsx";
import ShowChambers from "./chambers/ShowChambers.jsx";
import ShowStates from "./states/ShowStates.jsx";
import ShowDistricts from "./districts/ShowDistricts.jsx";
import ShowCandidates from "./candidates/ShowCandidates.jsx";
import useCountDistricts from "./districts/useCountDistricts.jsx";
import "../../css/selections.css";


export default function RenderSelections(
    {
        handleYearSelection, selectedYear,
        handleChamberSelection, selectedChamber,
        handleStateSelection, selectedState,
        handleDistrictSelection, selectedDistrict,
        handleCandidateSelection
    }
) {

    const districtCount = useCountDistricts(selectedChamber, selectedState, handleDistrictSelection);

    return (

        <div className="selections">

            <ShowYears
                onYearSelect={handleYearSelection}
            />

            {selectedYear && (
                <ShowChambers
                    year={selectedYear}
                    onChamberSelect={handleChamberSelection}
                />
            )}


            {selectedYear && selectedChamber && (
                <ShowStates
                    year={selectedYear}
                    chamber={selectedChamber}
                    onStateSelect={handleStateSelection}
                />
            )}

            {selectedYear && selectedChamber === "HOUSE" && selectedState && districtCount > 1 && (
                <ShowDistricts
                    year={selectedYear}
                    chamber={selectedChamber}
                    state={selectedState}
                    onDistrictSelect={handleDistrictSelection}
                />
            )}

            {selectedYear && selectedChamber && selectedState && selectedDistrict && (
                <ShowCandidates
                    year={selectedYear}
                    chamber={selectedChamber}
                    state={selectedState}
                    district={selectedDistrict}
                    onCandidateSelect={handleCandidateSelection}
                />
            )}

        </div>
    );

};