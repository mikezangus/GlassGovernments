import RenderContributionsTotal from "./RenderContributionsTotal";


export default function ContributionsTotal({ candidate }) {
    const { totalContAmt } = candidate;
    return (
        <RenderContributionsTotal
            totalContAmt={totalContAmt}
        />
    );
};
