import RenderContributionsTotal from "./RenderContributionsTotal";


export default function ShowContributionsTotal({ candidate }) {
    const { totalContributionAmount } = candidate;
    return (
        <RenderContributionsTotal
            totalContributionAmount={totalContributionAmount}
        />
    );
};