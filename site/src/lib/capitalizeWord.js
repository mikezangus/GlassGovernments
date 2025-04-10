export default function capitalizeWord(input) {
    const output = (input.match(/[^\s-.]+[\s-.]?/g) || [])
        .map(segment => {
            const delimiter = segment.match(/[\s-.,]$/)
                ? segment[segment.length - 1]
                : "";
            const word = delimiter
                ? segment.slice(0, -1)
                : segment;
            const upperCaseChar = word.charAt(0).toUpperCase()
            const lowerCaseChars = word.slice(1).toLowerCase()
            const reconstructedWord = upperCaseChar + lowerCaseChars + delimiter
            return reconstructedWord
    }).join("");
    return output
};
