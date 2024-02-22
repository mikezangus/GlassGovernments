import React from "react";
import Years from "./years/Years.jsx";
import Offices from "./offices/Offices.jsx";
import States from "./states/States.jsx";
import Districts from "./districts/Districts.jsx";
import Candidates from "./candidates/Candidates.jsx";
import useCountDistricts from "./districts/useCountDistricts.jsx";
import styles from "../../styles/Selections.module.css";


export default function Selections(
    {
        handleYearSelection, selectedYear,
        handleOfficeSelection, selectedOffice,
        handleStateSelection, selectedState,
        handleDistrictSelection, selectedDistrict,
        handleCandidateSelection
    }
) {

    const isPresidential = selectedOffice === "P";
    const districtCount = useCountDistricts(selectedYear, selectedOffice, selectedState, handleDistrictSelection);

    return (

        <div className={styles.selections}>

            <Years
                onYearSelect={handleYearSelection}
            />

            {selectedYear && (
                <Offices
                    year={selectedYear}
                    onOfficeSelect={(office) => {
                        handleOfficeSelection(office);
                        if (office === "P") {
                            handleStateSelection("US");
                            handleDistrictSelection("00");
                        }
                    }}
                />
            )}


            {selectedYear && !isPresidential && (
                <States
                    year={selectedYear}
                    office={selectedOffice}
                    selectedState={selectedState}
                    onStateSelect={handleStateSelection}
                />
            )}
            {selectedYear && selectedOffice === "H" && selectedState && districtCount > 1 && (
                <Districts
                    year={selectedYear}
                    office={selectedOffice}
                    state={selectedState}
                    selectedDistrict={selectedDistrict}
                    onDistrictSelect={handleDistrictSelection}
                />
            )}

            {selectedYear && selectedOffice && (selectedState || isPresidential ) && (selectedDistrict || isPresidential) && (
                <Candidates
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