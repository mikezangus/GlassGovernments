import React from "react";
import styles from "../styles/Header.module.css";


export default function Header() {
    return (
        <div className={styles.headerContainer}>
            <div className={styles.title}>
                <a href="https://glassgovernments.com">
                    Glass Governments
                </a>
            </div>
            <div className={styles.links}>
                <a
                    href="https://glassgovernments.com/about"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    About
                </a>
                <a
                    href="https://google.com"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    Submit feedback
                </a>
            </div>
        </div>
    );
};
