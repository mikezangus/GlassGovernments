import React from "react";
import styles from "../../../styles/Switch.module.css";


export default function RenderOffices({ offices, defaultOffice, handleOfficeClick }) {

    const officeNames = {
        H: "House",
        P: "Presidency",
        S: "Senate"
    };
    
    return (
        <div className={styles.switch}>
            <div className={styles.buttonsContainer}>
                {offices.map((office) => (
                    <button
                        key={office}
                        className={
                            `${styles.button}
                            ${defaultOffice === office
                                ? styles.active
                                : ""
                            }`
                        }
                        onClick={() => handleOfficeClick(office)}
                    >
                        {officeNames[office] || office}
                    </button>
                ))}
            </div>
        </div>
    );
};
