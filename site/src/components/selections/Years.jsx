import { useState } from "react";
import useFetchYears from "../../hooks/useFetchYears";
import styles from "../../styles/selections/Switch.module.css";


function Renderer({ years, defaultYear, handleYearClick }) {
    return (
        <div className={styles.switch}>
            <div className={styles.buttonsContainer}>
                {years.map((year) => (
                    <button
                        key={year}
                        className={
                            `${styles.button}
                            ${defaultYear === year
                                ? `${styles.active}`
                                : ""
                            }`
                        }
                        onClick={() => handleYearClick(year)}
                    >
                        {year}
                    </button>
                ))}
            </div>
        </div>
    );
};


export default function Years({ onYearSelect }) {

    const [years, setYears] = useState([]);
    const [defaultYear, setDefaultYear] = useState(null);

    useFetchYears(setYears, setDefaultYear, onYearSelect);

    const handleYearClick = (year) => {
        setDefaultYear(year);
        onYearSelect(year);
    };

    return (
        <Renderer
            years={years}
            defaultYear={defaultYear}
            handleYearClick={handleYearClick}
        />
    );

};
