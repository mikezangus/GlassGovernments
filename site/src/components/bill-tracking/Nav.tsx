import { Step } from "@/lib/types";
import styles from "@/styles/bill-tracking/Nav.module.css";


function BackButton(
    { setCurrentStep }:
    { setCurrentStep: React.Dispatch<React.SetStateAction<Step>> }
)
{
    function getPreviousStep(prev: Step): Step
    {
        return prev === 1 ? 1 : (prev - 1) as Step;
    }
    return (
        <button
            className={`${styles.button} ${styles.back}`}
            onClick={() => setCurrentStep(getPreviousStep)}
        >
            Back
        </button>
    );
}


function NextButton(
    { setCurrentStep }:
    { setCurrentStep: React.Dispatch<React.SetStateAction<Step>> }
)
{
    function getNextStep(prev: Step): Step
    {
        return prev === 3 ? 3 : ((prev + 1) as Step);
    }
    return (
        <button
            className={`${styles.button} ${styles.next}`}
            onClick={() => setCurrentStep(getNextStep)}
        >
            Next
        </button>
    );
}


export default function NavComponent(
    {
        currentStep,
        setCurrentStep
    }:
    {
        currentStep: Step;
        setCurrentStep: React.Dispatch<React.SetStateAction<Step>>;
    }
)
{
    return (
        <div className={styles.container}>
            {
                currentStep > 1 &&
                <BackButton setCurrentStep={setCurrentStep} />
            }
            {
                currentStep > 0 &&
                currentStep < 3 &&
                <NextButton setCurrentStep={setCurrentStep} />
            }
        </div>
    );
}
