import React from "react";
import ShowYears from "./years/ShowYears.jsx";
import ShowOffices from "./chambers/ShowOffices.jsx";
import ShowStates from "./states/ShowStates.jsx";
import ShowDistricts from "./districts/ShowDistricts.jsx";
import ShowCandidates from "./candidates/ShowCandidates.jsx";
import useCountDistricts from "./districts/useCountDistricts.jsx";
import "../../css/selections.css";


export default function RenderSelections(
    {
        handleYearSelection, selectedYear,
        handleOfficeSelection, selectedOffice,
        handleStateSelection, selectedState,
        handleDistrictSelection, selectedDistrict,
        handleCandidateSelection
    }
) {

    const districtCount = useCountDistricts(selectedYear, selectedOffice, selectedState, handleDistrictSelection);

    return (

        <div className="selections">

            <ShowYears
                onYearSelect={handleYearSelection}
            />

            {selectedYear && (
                <ShowOffices
                    year={selectedYear}
                    onOfficeSelect={handleOfficeSelection}
                />
            )}


            {selectedYear && selectedOffice != "P" && (
                <ShowStates
                    year={selectedYear}
                    office={selectedOffice}
                    onStateSelect={handleStateSelection}
                />
            )}
            {selectedYear && selectedOffice === "H" && selectedState && districtCount > 1 && (
                <ShowDistricts
                    year={selectedYear}
                    office={selectedOffice}
                    state={selectedState}
                    onDistrictSelect={handleDistrictSelection}
                />
            )}

            {selectedYear && selectedOffice && selectedState && selectedDistrict && (
                <ShowCandidates
                    year={selectedYear}
                    office={selectedOffice}
                    state={selectedState}
                    district={selectedDistrict}
                    onCandidateSelect={handleCandidateSelection}
                />
            )}

        </div>
    );

};