import usa_states_all from "./usa_states_all.json";


export default function showStateName(stateCode) {
    const stateName = usa_states_all[stateCode] || stateCode;
    return stateName
};