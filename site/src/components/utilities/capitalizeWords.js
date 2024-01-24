export default function capitalizeWords(input) {
    return input.split(/[\s-]/).map(word =>
        word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
    ).join(" ");
};