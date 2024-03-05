import { useState } from "react";
import useFetchDistricts from "../../hooks/useFetchDistricts";
import styles from "../../styles/selections/Dropdown.module.css";


function Renderer({ districts, selectedDistrict, isOpen, toggleDropdown, handleDistrictClick }) {
    return (
        <div className={styles.dropdown}>
            <div className={styles.container}>
                <button
                    className={
                        `${styles.button}
                        ${isOpen
                            ? styles.active
                            : ""
                        }`
                    }
                    onClick={toggleDropdown}
                >
                    {
                        selectedDistrict
                            ? `District: ${parseInt(selectedDistrict, 10).toString()}`
                            : "Select a district ▽"
                    }
                </button>
                {isOpen && (
                    <div className={styles.menu}>
                        {districts.map((district) => (
                            <button
                                className={styles.item}
                                key={district}
                                onClick={() => handleDistrictClick(district)}
                            >
                                {`District ${parseInt(district, 10).toString()}`}
                            </button>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};


export default function Districts({ year, office, state, selectedDistrict, onDistrictSelect }) {

    const [districts, setDistricts] = useState([]);
    const [isOpen, setIsOpen] = useState(false);

    useFetchDistricts(year, office, state, setDistricts);

    const toggleDropdown = () => setIsOpen(!isOpen);
    const handleDistrictClick = (district) => {
        onDistrictSelect(district);
        setIsOpen(false);
    };

    return (
        <Renderer
            districts={districts}
            selectedDistrict={selectedDistrict}
            isOpen={isOpen}
            toggleDropdown={toggleDropdown}
            handleDistrictClick={handleDistrictClick}
        />
    );
    
};
