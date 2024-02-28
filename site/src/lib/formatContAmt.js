export default function formatContAmt(amount) {
    return (
        amount >= 10000000 ? `${(amount / 1000000).toFixed(1)}M` : // $60,900,000 => $60.9M
        amount >= 1000000 ? `${(amount / 1000000).toFixed(2)}M` : // $6,090,000 => $6.09M
        amount >= 100000 ? `${(amount / 1000).toFixed(0)}K` : // $609,000 => $609K
        amount >= 10000 ? `${(amount / 1000).toFixed(1)}K` : // $60,900 => $60.9K
        amount >= 1000 ? `${(amount / 1000).toFixed(2)}K` : // $6,090 => $6.09K
        `${amount}` // $609 => $609
    );
};