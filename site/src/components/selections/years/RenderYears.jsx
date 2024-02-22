import React from "react";
import styles from "../../../styles/Switch.module.css";


export default function RenderYears({ years, defaultYear, handleYearClick }) {
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
