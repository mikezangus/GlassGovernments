"use client";


import { useState } from "react";
import Link from "next/link";
import styles from "../styles/Header.module.css";



export default function Header()
{
    const [open, setOpen] = useState(false);
    return (
        <header className={styles.container}>
            <Link href="/" className={styles.title}>
                Glass Governments
            </Link>
            <nav className={styles.routes} aria-label="primary">
                <Link href="/bill-tracking">Bill Tracking</Link>
                <Link href="/funding">Candidate Fundings</Link>
                <Link href="/votes">Vote Predictions</Link>
            </nav>
            <button
                className={styles.hamburger}
                aria-label="Toggle menu"
                aria-expanded={open}
                onClick={() => setOpen(prev => !prev)}
            >
                <span />
            </button>
            <nav
                className={`${styles.drawer} ${open ? styles.show : ""}`}
                aria-label="mobile"
                onClick={() => setOpen(false)}
            >
                <Link href="/bill-tracking">Bill Tracking</Link>
                <Link href="/funding">Candidate Fundings</Link>
                <Link href="/votes">Vote Predictions</Link>
            </nav>
        </header>
    );
}
