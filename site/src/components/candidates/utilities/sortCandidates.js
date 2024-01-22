export default function sortCandidates(candidates) {
    return candidates.sort((a, b) => b.totalContributionAmount - a.totalContributionAmount);
};