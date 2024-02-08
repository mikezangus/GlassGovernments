import RenderBio from "./RenderBio";


export default function ShowBio({ state, district, candidate }) {
    return (
        <RenderBio
            state={state}
            district={district}
            candidate={candidate}
        />
    );
};