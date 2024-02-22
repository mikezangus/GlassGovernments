import RenderContributionsTotal from "./RenderContributionsTotal";


export default function ContributionsTotal({ candidate }) {
    const { totalContributionAmount } = candidate;
    return (
        <RenderContributionsTotal
            totalContributionAmount={totalContributionAmount}
        />
    );
};
