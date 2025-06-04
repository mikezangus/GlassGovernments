import { Step, TokenItem } from "@/lib/types";
import styles from "@/styles/LawTracking.module.css";


function handleForward(
    currentStep: Step,
    setCurrentStep: (step: Step) => void,
    tokenItems: TokenItem[],
    setTokenItems: (tokenItems: TokenItem[]) => void,
): void
{
    if (currentStep === Step.Tokens) {
        const filteredTokens = tokenItems.filter(t => t.token.trim() !== "");
        setTokenItems(filteredTokens);
    }
    if (currentStep < Step.Contact) {
        setCurrentStep(currentStep + 1);
    }
}


function handleBackward(
    currentStep: Step,
    setCurrentStep: (step: Step) => void
): void
{
    if (currentStep > Step.Tokens) {
        setCurrentStep(currentStep - 1);
    } 
}

export default function NavComponent(
    {
        currentStep,
        setCurrentStep,
        tokenItems,
        setTokenItems
    }:
    {
        currentStep: Step;
        setCurrentStep: (step: Step) => void;
        tokenItems: TokenItem[];
        setTokenItems: (tokenItems: TokenItem[]) => void;
    }
)
{
    return (
        <div className={styles.navigationButtons}>
            <button
                onClick={() => handleBackward(
                    currentStep,
                    setCurrentStep
                )}
                disabled={currentStep === Step.Tokens}
                className={styles.navButton}
            >
                {"<-"}
            </button>
            <button
                onClick={() => handleForward(
                    currentStep,
                    setCurrentStep,
                    tokenItems,
                    setTokenItems
                )}
                disabled={currentStep === Step.Contact}
                className={styles.navButton}
            >
                {"->"}
            </button>
        </div>
    );
}
