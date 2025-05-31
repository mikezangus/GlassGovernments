import { TokenItem } from "./types";
import styles from "@/styles/LawTracking.module.css";


export default function TokenComponent(
    {
        tokenEntry,
        deleteToken
    }:
    {
        tokenEntry: TokenItem;
        deleteToken: (token: string) => void;
    }
)
{
    const { token, states } = tokenEntry;
    return (
        <div className={styles.tokenContainer}>
            <div className={styles.tokenTextContainer}>
                <div className={styles.tokenNameContainer}>
                    {token}
                </div>
                <div className={styles.tokenStatesContainer}>
                    {
                        states
                            .slice()
                            .sort((a, b) => a.localeCompare(b))
                            .join(", ")
                    }
                </div>
            </div>
            <button
                className={styles.tokenContainerDeleteButton}
                onClick={() => deleteToken(token)}
            >
                x
            </button>
        </div>
    );
}
