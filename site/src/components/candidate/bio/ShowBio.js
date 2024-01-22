import useFetchBio from "./useFetchBio";
import RenderBio from "./RenderBio";


export default function ShowBio({ chamber, state, district, candidate }) {
    useFetchBio(chamber, state, district, candidate);
    return (
        <RenderBio
            state={state}
            district={district}
            candidate={candidate}
        />
    );
};