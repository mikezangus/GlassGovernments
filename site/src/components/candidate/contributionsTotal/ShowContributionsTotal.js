import useFetchContributionsTotal from "./useFetchContributionsTotal";
import RenderContributionsTotal from "./RenderContributionsTotal";


export default function ShowContributionsTotal({ chamber, state, district, candidate }) {
    useFetchContributionsTotal(chamber, state, district, candidate);
    return (
        <RenderContributionsTotal
            candidate={candidate}
        />
    );
};