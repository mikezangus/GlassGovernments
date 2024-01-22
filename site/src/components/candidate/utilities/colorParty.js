export default function colorParty(party) {
    switch (party) {
        case "DEMOCRATIC": return "blue";
        case "GREEN": return "green";
        case "INDEPENDENT": return "purple";
        case "LIBERTARIAN": return "gold";
        case "REPUBLICAN": return "red";
        default: return "gray";
    };
};