import { useState } from "react";
import useFetchYears from "../../hooks/selections/useFetchYears";
import styles from "../../styles/selections/Switch.module.css";


function RenterItem({ year, defaultYear, handleYearClick }) {
    return (
        <button
            key={year}
            className={`
                ${styles.button}
                ${
                    defaultYear === year
                        ? `${styles.active}`
                        : ""
                }
            `}
            onClick={() => handleYearClick(year)}
        >
            {year}
        </button>
    );
};


function Renderer({ years, defaultYear, handleYearClick }) {
    return (
        <div className={styles.switchContainer}>
            <div className={styles.buttonsContainer}>
                {years.map((year) => (
                    <RenterItem
                        year={year}
                        defaultYear={defaultYear}
                        handleYearClick={handleYearClick}
                    />
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
