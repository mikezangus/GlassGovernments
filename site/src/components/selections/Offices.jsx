import { useState } from "react";
import useFetchOffices from "../../hooks/useFetchOffices";
import styles from "../../styles/selections/Switch.module.css";


function RenderItem({ office, defaultOffice, handleOfficeClick }) {
    const officeNames = {
        H: "House",
        P: "Presidency",
        S: "Senate"
    };
    return (
        <button
            key={office}
            className={`
                ${styles.button}
                ${
                    defaultOffice === office
                        ? styles.active
                        : ""
                }
            `}
            onClick={() => handleOfficeClick(office)}
        >
            {officeNames[office] || office}
        </button>
    );
};


function Renderer({ offices, defaultOffice, handleOfficeClick }) {
    return (
        <div className={styles.switchContainer}>
            <div className={styles.buttonsContainer}>
                {offices.map((office) => (
                    <RenderItem
                        office={office}
                        defaultOffice={defaultOffice}
                        handleOfficeClick={handleOfficeClick}
                    />
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
