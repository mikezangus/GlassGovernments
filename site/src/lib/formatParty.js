export default function formatParty(partyRaw) {
    const party = partyRaw.toLowerCase()
    if (party === "dem") return "Democrat";
    if (party === "gre") return "Green";
    if (party === "ind" || party === "npa" || party === "nne" || party === "non" || party === "oth") return "Independent";
    if (party === "lib") return "Libertarian";
    if (party === "rep") return "Republican";
    return party
};