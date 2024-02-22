import React from "react";
import styles from "../../../styles/Dropdown.module.css";


export default function RenderDistricts({ districts, selectedDistrict, isOpen, toggleDropdown, handleDistrictClick }) {
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
