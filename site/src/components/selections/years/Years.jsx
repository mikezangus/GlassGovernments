import { useState } from "react";
import useFetchYears from "./useFetchYears";
import RenderYears from "./RenderYears";


export default function Years({ onYearSelect }) {

    const [years, setYears] = useState([]);
    const [defaultYear, setDefaultYear] = useState(null);

    useFetchYears(setYears, setDefaultYear, onYearSelect);

    const handleYearClick = (year) => {
        setDefaultYear(year);
        onYearSelect(year);
    };

    return (
        <RenderYears
            years={years}
            defaultYear={defaultYear}
            handleYearClick={handleYearClick}
        />
    );

};
