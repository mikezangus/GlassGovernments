import RenderContributionsTotal from "./RenderContributionsTotal";


export default function ShowContributionsTotal({ candidate }) {
    const { totalContributionAmount, x, y, z } = candidate;
    return (
        <RenderContributionsTotal
            totalContributionAmount={totalContributionAmount}
        />
    );
};