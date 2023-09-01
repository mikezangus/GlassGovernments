document.addEventListener("DOMContentLoaded", function() {
    const politicians = [
        {
            id: 1,
            name: "Chris Deluzio",
            csvFile: "2022_Deluzio_output.csv",
            incumbency: "Incumbent",
            party: "Democrat",
            constituency: "PA-17",
            photoUrl: "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Rep._Chris_Deluzio_-_118th_Congress.jpg/1280px-Rep._Chris_Deluzio_-_118th_Congress.jpg",
        },
        {
            id: 2,
            name: "Summer Lee",
            csvFile: "2022_Lee_output.csv",
            incumbency: "Incumbent",
            party: "Democrat",
            constituency: "PA-18",
            photoUrl: "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Rep._Summer_Lee_-_118th_Congress.jpg/1280px-Rep._Summer_Lee_-_118th_Congress.jpg",
        },
        {
            id: 3,
            name: "Mike Kelly",
            csvFile: "2022_Kelly_output.csv",
            incumbency: "Incumbent",
            party: "Republican",
            constituency: "PA-16",
            photoUrl: "https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Mike_Kelly%2C_Official_Portrait%2C_112th_Congress.jpg/1024px-Mike_Kelly%2C_Official_Portrait%2C_112th_Congress.jpg",
        },
    ];
    politicians.forEach(politician => {
        fetchCSVData(politician.csvFile, politician);
    });
});

function fetchCSVData(csvFile, politician) {
    fetch(csvFile)
        .then(response => response.text())
        .then(csvData => {
            handleCSVData(csvData, politician);
        });
}

function handleCSVData(csvData, politician) {
    Papa.parse(csvData, {
        header: true,
        complete: function(results) {
            const data = results.data;
            const { totalFundingOutsidePA } = extractData(data);
            updatePhoto(politician.photoUrl, politician);
            updateName(politician.name, politician);
            updateIncumbency(politician.incumbency, politician);
            updateParty(politician.party, politician);
            updateConstituency(politician.constituency, politician);
            updateFundingAmount(totalFundingOutsidePA, politician);
        }
    });
}

function extractData(data) {
    let name = "";
    let incumbency = "";
    let constituency = "";
    let party = "";
    let totalFundingOutsidePA = 0;
    if (data.length > 0) {
        const firstEntry = data[0];
        name = firstEntry.name;
        incumbency = firstEntry.incumbency;
        constituency = firstEntry.constituency;
        party = firstEntry.party;
        data.forEach(state => {
            const totalContributionAmount = parseFloat(state.total_contribution_amount);
            if(!isNaN(totalContributionAmount) && state.contributor_state !== "PA") {
                totalFundingOutsidePA += totalContributionAmount;
            }
        });
    }
    return { name, incumbency, constituency, party, totalFundingOutsidePA };
}

function updatePhoto(photoUrl, politician) {
    const photoElement = document.getElementById(`photo-${politician.id}`);
    photoElement.src = photoUrl;
}

function updateName(name, politician) {
    const nameElement = document.querySelector(`#politician-info-${politician.id} .name`);
    nameElement.textContent = name;
}

function updateIncumbency(incumbency, politician) {
    const incumbencyElement = document.querySelector(`#politician-info-${politician.id} .incumbency`);
    incumbencyElement.textContent = incumbency;
}

function updateParty(party, politician) {
    const partyElement = document.querySelector(`#politician-info-${politician.id} .party`);
    partyElement.textContent = party;
}

function updateConstituency(constituency, politician) {
    const constituencyElement = document.querySelector(`#politician-info-${politician.id} .constituency`);
    constituencyElement.textContent = constituency;
}

function updateFundingAmount(totalFundingOutsidePA, politician) {
    const fundingAmountElement = document.querySelector(`#politician-info-${politician.id} .funding-amount`);
    const formattedAmount = formatAmountWithCommas(totalFundingOutsidePA);
    fundingAmountElement.textContent = `$${formattedAmount} in foreign funding`;
}

function formatAmountWithCommas(amount) {
    return amount.toLocaleString("en-US", {maximumFractionDigits: 2});
}
