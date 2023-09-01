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
    {
        id: 4,
        name: "Brian Fitzpatrick",
        csvFile: "2022_Fitzpatrick_output.csv",
        incumbency: "Incumbent",
        party: "Republican",
        constituency: "PA-01",
        photoUrl: "https://upload.wikimedia.org/wikipedia/commons/3/3a/Brian_Fitzpatrick_official_congressional_photo.jpg",
    },
    {
        id: 5,
        name: "Brendan Boyle",
        csvFile: "2022_Boyle_output.csv",
        incumbency: "Incumbent",
        party: "Democrat",
        constituency: "PA-02",
        photoUrl: "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Brendan_Boyle_-_2018-05-21_ec_0004.jpg/1024px-Brendan_Boyle_-_2018-05-21_ec_0004.jpg",
    },
];

document.addEventListener("DOMContentLoaded", function() {
    politicians.forEach(politician => {
        fetchCSVData(politician);
    });
    const sortButton = document.getElementById("sort-button");
    sortButton.addEventListener("click", toggleSort);
});

async function fetchCSVData(politician) {
    try {
        const response = await fetch(politician.csvFile);
        const csvData = await response.text();
        handleCSVData(csvData, politician);
    } catch (error) {
        console.error(`Error fetching CSV data for ${politician.name}: ${error}`);
    }
}

function handleCSVData(csvData, politician) {
    Papa.parse(csvData, {
        header: true,
        complete: function(results) {
            const data = results.data;
            const { totalFundingOutsidePA } = extractData(data);
            politician.totalFundingOutsidePA = totalFundingOutsidePA;
            updateUI(politician, totalFundingOutsidePA);
        }
    });
}

function extractData(data) {
    let totalFundingOutsidePA = 0;
    if (data && data.length > 0) {
        data.forEach(state => {
            const totalContributionAmount = parseFloat(state.total_contribution_amount);
            if(!isNaN(totalContributionAmount) && state.contributor_state !== "PA") {
                totalFundingOutsidePA += totalContributionAmount;
            }
        });
    }
    return { totalFundingOutsidePA };
}

let sortByMostFunding = true;

function toggleSort() {
    sortByMostFunding = !sortByMostFunding;
    sortPoliticians();
}

// function sortPoliticians() {
//     politicians.sort((a, b) => {
//         const fundingA = a.totalFundingOutsidePA;
//         const fundingB = b.totalFundingOutsidePA;
//         if (sortByMostFunding) {
//             return fundingB - fundingA;
//         } else {
//             return fundingA - fundingB;
//         }
//     });
//     politicians.forEach((politician, index) => {
//         const position = index + 1;
//         updateUI(politician, politician.totalFundingOutsidePA, position);
//     });
// }

function sortPoliticians() {
    const politicianContainer = document.getElementById('politicians-container');
    politicianContainer.innerHTML = '';

    politicians.sort((a, b) => {
        const fundingA = a.totalFundingOutsidePA;
        const fundingB = b.totalFundingOutsidePA;
        if (sortByMostFunding) {
            return fundingB - fundingA;
        } else {
            return fundingA - fundingB;
        }
    });

    politicians.forEach((politician, index) => {
        const position = index + 1;
        updateUI(politician, politician.totalFundingOutsidePA, position);
    });
}

// function updateUI(politician, totalFundingOutsidePA, position) {
//     const politicianInfo = document.getElementById(`politician-info-${politician.id}`);
//     politicianInfo.querySelector(".name").textContent = politician.name;
//     politicianInfo.querySelector(".incumbency").textContent = politician.incumbency;
//     politicianInfo.querySelector(".party").textContent = politician.party;
//     politicianInfo.querySelector(".constituency").textContent = politician.constituency;

//     const fundingAmountElement = politicianInfo.querySelector(".funding-amount");
//     const formattedAmount = formatAmountWithCommas(totalFundingOutsidePA);
//     fundingAmountElement.textContent = `$${formattedAmount} in foreign funding`;

//     const photoElement = politicianInfo.querySelector(".photo img");
//     photoElement.src = politician.photoUrl;

//     const positionElement = politicianInfo.querySelector(".position");
//     positionElement.textContent = `Position: ${position}`;
// }

function updateUI(politician, totalFundingOutsidePA, position) {
    const politicianContainer = document.getElementById('politicians-container');

    const politicianElement = document.createElement('div');
    politicianElement.id = `politician-info-${politician.id}`;

    politicianElement.innerHTML = `
        <div class="name">${politician.name}</div>
        <div class="incumbency">${politician.incumbency}</div>
        <div class="party">${politician.party}</div>
        <div class="constituency">${politician.constituency}</div>
        <div class="funding-amount">$${formatAmountWithCommas(totalFundingOutsidePA)} in foreign funding</div>
        <img class="photo" src="${politician.photoUrl}" />
        <div class="position">Position: ${position}</div>
    `;

    politicianContainer.appendChild(politicianElement);
}

function formatAmountWithCommas(amount) {
    return amount.toLocaleString("en-US", {maximumFractionDigits: 2});
}
