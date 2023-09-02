
let sortByMostFunding = true;

document.addEventListener("DOMContentLoaded", init);

async function init() {
    await Promise.all(politicians.map(fetchCSVData));
    document.getElementById("sort-button").addEventListener("click", toggleSort);
    sortPoliticians();
}

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
        complete: results => {
            const { totalFunding, totalFundingOutsidePA, percentFundingOutsidePA } = extractData(results.data);
            politician.totalFunding = totalFunding;
            politician.totalFundingOutsidePA = totalFundingOutsidePA;
            politician.percentFundingOutsidePA = percentFundingOutsidePA;
        }
    });
}

function extractData(data) {
    let totalFunding = 0;
    let totalFundingOutsidePA = data.reduce((total, state) => {
        const amount = parseFloat(state.total_contribution_amount);
        totalFunding += (!isNaN(amount)) ? amount : 0;
        if (!isNaN(amount) && state.contributor_state !== "PA") {
            total += amount;
        }
            return total
    }, 0);
    return {
        totalFunding,
        totalFundingOutsidePA,
        percentFundingOutsidePA: (totalFundingOutsidePA / totalFunding) * 100
    }
}

function toggleSort() {
    sortByMostFunding = !sortByMostFunding;
    sortPoliticians();
}

function sortPoliticians() {
    const politicianContainer = document.getElementById('politicians-container');
    politicianContainer.innerHTML = '';
    politicians.sort((a, b) => sortByMostFunding ? b.totalFundingOutsidePA - a.totalFundingOutsidePA : a.totalFundingOutsidePA - b.totalFundingOutsidePA);
    politicians.forEach(updateUI);
}

function updateUI(politician, index) {
    const politicianContainer = document.getElementById('politicians-container');

    const politicianElement = document.createElement('div');
    politicianElement.className = `politician-info`;
    politicianElement.id = `politician-info-${politician.id}`;

    politicianElement.innerHTML = `
        <div class="photo">
            <div class="circle-crop">
                <img src="${politician.photoUrl}" alt="${politician.name}" id="photo-${politician.id}">
            </div>
            <div class="info">
                <div class="row">
                    <p class="name">${politician.name}</p>
                </div>
                <div class="row">
                    <p class="incumbency">${politician.incumbency}</p>
                    <p class="party">${politician.party},</p>
                    <p class="constituency">${politician.constituency}</p>
                </div>
                <div class="row">
                    <p class="funding-amount">$${formatAmountWithCommas(politician.totalFundingOutsidePA)} foreign funding</p>
                </div>  
                <div class="row">
                    <p class="total-funding-amount">$${formatAmountWithCommas(politician.totalFunding)} total funding</p>
                </div>  
                <div class="row">
                    <p class="funding-percentage">${politician.percentFundingOutsidePA.toFixed(2)}% foreign funded</p>
                </div>
            </div>
        </div>
    `;

    politicianContainer.appendChild(politicianElement);
}

function formatAmountWithCommas(amount) {
    return amount.toLocaleString("en-US", {maximumFractionDigits: 2});
}
