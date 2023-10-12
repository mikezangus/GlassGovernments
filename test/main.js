document.addEventListener("DOMContentLoaded", () => {
    fetchDataFromMongoDB();
});

async function fetchDataFromMongoDB() {
    try {
        const response = await fetch("/data");
        if(!response.ok) {
            throw new Error("Failed to fetch data")
        }
        const data = await response.json();
        const dataList = document.getElementById("mongoData")
        data.forEach(item => {
            const listItem = document.createElement("li");
            listItem.textContent = `${item.state}`;
            dataList.appendChild(listItem);
        });
    } catch (error) {
        console.error("Error fetchind data:", error)
    }
}