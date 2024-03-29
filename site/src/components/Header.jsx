import React from "react";
import styles from "../styles/Header.module.css";


export default function Header() {
    return (
        <div className={styles.headerContainer}>
            <div className={styles.headerItemsContainer}>
                <div className={styles.titleContainer}>
                    <a href="https://glassgovernments.com">
                        Glass Governments
                    </a>
                </div>
                <div className={styles.pagesContainer}>
                    <a
                        href="https://github.com/mikezangus/glassgovernments"
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        About
                    </a>
                    <a
                        href="https://docs.google.com/forms/d/e/1FAIpQLSf3hDdCeb_FaMb8p1qCjSwm8nGu-o_vDhWH5sKNbg6LEEC8oQ/viewform?usp=sf_link"
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        Submit feedback
                    </a>
                </div>
            </div>
        </div>
    );
};
