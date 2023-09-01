document.addEventListener("DOMContentLoaded", function() {
    fetchCSVData("2022_Deluzio_output.csv");
});

function fetchCSVData(csvFile) {
    fetch(csvFile)
        .then(response => response.text())
        .then(csvData => {
            handleCSVData(csvData);
        });
}

function handleCSVData(csvData) {
    Papa.parse(csvData, {
        header: true,
        complete: function(results) {
            const data = results.data;
            const { totalFundingOutsidePA } = extractData(data);
            const name = "Chris Deluzio";
            const incumbency = "Incumbent";
            const party = "Democrat, ";
            const constituency = "PA-17";
            updatePhoto(totalFundingOutsidePA);
            updateName(name);
            updateIncumbency(incumbency);
            updateParty(party);
            updateConstituency(constituency);
            updateFundingAmount(totalFundingOutsidePA);
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

function updatePhoto(totalFundingOutsidePA) {
    const photoElement = document.getElementById("photo");
    const wikipediaPhotoUrl = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Rep._Chris_Deluzio_-_118th_Congress.jpg/1280px-Rep._Chris_Deluzio_-_118th_Congress.jpg";
    photoElement.src = wikipediaPhotoUrl;
}

function updateName(name) {
    document.querySelector(".name").textContent = name;
}

function updateIncumbency(incumbency) {
    document.querySelector(".incumbency").textContent = incumbency;
}

function updateParty(party) {
    document.querySelector(".party").textContent = party;
}

function updateConstituency(constituency) {
    document.querySelector(".constituency").textContent = constituency;
}

function updateFundingAmount(totalFundingOutsidePA) {
    const fundingAmountElement = document.querySelector(".funding-amount");
    const formattedAmount = formatAmountWithCommas(totalFundingOutsidePA);
    fundingAmountElement.textContent = `$${formattedAmount} in foreign funding`;
}


function formatAmountWithCommas(amount) {
    return amount.toLocaleString("en-US", {maximumFractionDigits: 2});
}