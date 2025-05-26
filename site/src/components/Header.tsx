import styles from "../styles/Header.module.css";
import Link from "next/link";


export default function Header()
{
    return (
        <div className={styles.headerContainer}>
            <Link href="/" className={styles.titleContainer}>
                Glass Governments
            </Link>
            <div className={styles.productsContainer}>
                <Link href="/law-tracking">Law Tracking</Link>
                <Link href="/funding">Candidate Fundings</Link>
                <Link href="/votes">Vote Predictions</Link>
            </div>
        </div>
    );
}
