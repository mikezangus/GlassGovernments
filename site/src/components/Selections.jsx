import React from "react";
import Years from "./selections/Years.jsx";
import Offices from "./selections/Offices.jsx";
import States from "./selections/States.jsx";
import Districts from "./selections/Districts.jsx";
import Candidates from "./selections/Candidates.jsx";
import useCountDistricts from "../hooks/useCountDistricts.jsx";
import styles from "../styles/selections/Selections.module.css";


export default function Selections(
    {
        handleYearSelection, selectedYear,
        handleOfficeSelection, selectedOffice,
        handleStateSelection, selectedState,
        handleDistrictSelection, selectedDistrict,
        handleCandidateSelection, selectedCandidate
    }
) {

    const isPresidential = selectedOffice === "P";
    const districtCount = useCountDistricts(selectedYear, selectedOffice, selectedState, handleDistrictSelection);

    return (

        <div className={styles.selectionsContainer}>

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
                    selectedCandidate={selectedCandidate}
                    onCandidateSelect={handleCandidateSelection}
                />
            )}

        </div>
    );

};
