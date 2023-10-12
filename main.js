import { fetchPoliticianData } from "./api"

let sortByMostFunding = true;

document.addEventListener("DOMContentLoaded", init);

async function init() {
    let politicians = await fetchPoliticianData();
    document.getElementById("sort-button").addEventListener("click", toggleSort);
    sortPoliticians();
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
