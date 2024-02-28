import { useState } from "react";
import useFetchOffices from "../../hooks/useFetchOffices";
import styles from "../../styles/Switch.module.css";


function Renderer({ offices, defaultOffice, handleOfficeClick }) {

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


export default function Offices({ year, onOfficeSelect }) {

    const [offices, setOffices] = useState([]);
    const [defaultOffice, setDefaultOffice] = useState(null);

    useFetchOffices(year, setOffices, setDefaultOffice, onOfficeSelect);

    const handleOfficeClick = (office) => {
        setDefaultOffice(office);
        onOfficeSelect(office);
    };

    return (
        <Renderer
            offices={offices}
            defaultOffice={defaultOffice}
            handleOfficeClick={handleOfficeClick}
        />
    );

};
