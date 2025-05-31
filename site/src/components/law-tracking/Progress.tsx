import styles from "@/styles/LawTracking.module.css";


export default function ProgressComponent(
    { i, len }:
    { i: number; len: number }
)
{
    return (
        <div className={styles.progressBarContainer}>
            {`${i}/${len}`}
        </div>
    );
}
