fetch('2022_Deluzio_output.csv')
    .then(response => response.text())
    .then(csvData => {
        Papa.parse(csvData, {
            header: true,
            complete: function(results) {
                const data = results.data;
                const stateDataContainer = document.getElementById('state-data');
                data.forEach(state => {
                    const stateElement = document.createElement('div');
                    stateElement.classList.add('state-info');
                    stateElement.innerHTML = `
                        <h2>${state.contributor_state}</h2>
                        <p>Total Contributions: $${parseFloat(state.total_contribution_amount).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2})}</p>
                        <p>Individual Contributions: $${parseFloat(state.ind_contribution_amount).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2})}</p>
                        <p>PAC Contributions: $${parseFloat(state.pac_contribution_amount).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2})}</p>
                    `;
                    stateDataContainer.appendChild(stateElement);
                });
            }
        });
    });