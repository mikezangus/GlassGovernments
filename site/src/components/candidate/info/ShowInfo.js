import useFetchInfo from "./useFetchInfo";
import RenderInfo from "./RenderInfo";


export default function ShowInfo({ chamber, state, district, candidate }) {
    useFetchInfo(chamber, state, district, candidate);
    return RenderInfo(state, district, candidate);
};