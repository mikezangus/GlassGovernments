export default function colorParty(party) {
    switch (party) {
        case "DEMOCRAT": return "darkblue";
        case "GREEN": return "darkgreen";
        case "INDEPENDENT": return "purple";
        case "LIBERTARIAN": return "gold";
        case "REPUBLICAN": return "darkred";
        default: return "darkgrey";
    };
};