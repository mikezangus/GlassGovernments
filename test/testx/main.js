document.addEventListener("DOMContentLoaded", init);

function init() {
    console.log("test 1");
    updateDateTime();
    console.log("test 2");
    setInterval(updateDateTime, 1000);
    console.log("test 3");
    pullPhoto();
    console.log("test 4");
    fetchMongoData();
    console.log("test 5");
}

function updateDateTime() {
    const datetimeElement = document.getElementById("datetime");
    const now = new Date();
    const options = {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit"
    };
    const formattedDateTime = now.toLocaleDateString("en-US", options);
    datetimeElement.textContent = formattedDateTime;
}

function pullPhoto() {
    const wikipediaPhotoElement = document.getElementById("wikipediaPhoto");
    const wikipediaPhotoUrl = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Rex_Tillerson_official_portrait.jpg/1280px-Rex_Tillerson_official_portrait.jpg";
    const imgElement = document.createElement("img");
    imgElement.src = wikipediaPhotoUrl;
    wikipediaPhotoElement.appendChild(imgElement);
}

function fetchMongoData() {
    axios.get("https://us-east-1.aws.data.mongodb-api.com/app/data-xzsks/endpoint/data/v1/action/findOne")
        .then(function (response) {
            const mongoDataElement = document.getElementById("mongoData");
            mongoDataElement.textContent = JSON.stringify(response.data, null, 2);
        })
        .catch(function (error) {
            console.log(error);
        });
}