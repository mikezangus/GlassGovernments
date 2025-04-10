export default function colorParty(party) {
    switch (party) {
        case "Democrat": return "darkblue";
        case "Green": return "darkgreen";
        case "Independent": return "purple";
        case "Libertarian": return "gold";
        case "Republican": return "darkred";
        default: return "darkgrey";
    };
};
