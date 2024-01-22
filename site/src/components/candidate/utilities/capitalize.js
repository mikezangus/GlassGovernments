export default function capitalize(input) {
    return input.split(/[\s-]/).map(word =>
        word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
    ).join(" ");
};