import showStateName from "./showStateName";


export default function formatConstituency(state, constituency) {
    const stateName = showStateName(state);
    if (constituency.toLowerCase() === "senate") return `U.S. Senate - ${stateName}`;
    if (constituency === "00") return `${stateName} at large`;
    return `${stateName} District ${parseInt(constituency, 10).toString()}`;
};