import RenderContributionsTotal from "./RenderContributionsTotal";


export default function ContributionsTotal({ candidate }) {
    const { totalContAmt } = candidate;
    console.log(totalContAmt)
    return (
        <RenderContributionsTotal
            totalContAmt={totalContAmt}
        />
    );
};
