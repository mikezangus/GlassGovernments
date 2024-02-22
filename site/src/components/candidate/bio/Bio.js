import RenderBio from "./RenderBio";


export default function Bio({ state, district, candidate }) {
    return (
        <RenderBio
            state={state}
            district={district}
            candidate={candidate}
        />
    );
};
