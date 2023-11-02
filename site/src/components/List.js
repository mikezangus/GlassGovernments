import React, { useState, useEffect } from "react"

function formatAmount(amount) {
    if (amount >= 10000000) {
        return `${(amount / 1000000).toFixed(1)}M`
        // $60,900,000 => $60.9M
    } else if (amount >= 1000000) {
        return `${(amount / 1000000).toFixed(2)}M`
        // $6,090,000 => $6.09M
    } else if (amount >= 100000) {
        return `${(amount / 1000).toFixed(0)}K`
        // $609,000 => $609K
    } else if (amount >= 10000) {
        return `${(amount / 1000).toFixed(1)}K`
        // $60,900 => $60.9K
    } else if (amount >= 1000) {
        return `${(amount / 1000).toFixed(2)}K`
        // $6,090 => $6.09K
    } else {
        return `${amount}`
        // $609 => $609
    }
}

function List() {
    const [isOpen, setIsOpen] = useState(false)
    const [options, setOptions] = useState([])
    
    useEffect(() => {
        fetch("http://localhost:4000/api/lastnames")
            .then(response => response.json())
            .then(data => {
                const sortedData = [...data].sort((a, b) => b.totalFunding - a.totalFunding)
                setOptions(sortedData)
            })
            .catch(error => console.error("Error fetching data:", error))
        }, [])

    const toggleDropdown = () => {
        setIsOpen(prevState => !prevState)
    }

    return (
        <main>
            <div className="list-container">
                <h2 className="list-title">Politicians</h2>
                <div className="dropdown">
                    <button onClick={toggleDropdown}>
                        Click to select a politician
                    </button>
                    {isOpen && (
                        <div className="dropdown-menu">
                            {options.map(option => (
                                <button key={option._id} onClick={() => {
                                    toggleDropdown()
                                }}>
                                    {console.log(option._id, option.totalFunding.toLocaleString())}
                                    {option._id} - ${formatAmount(option.totalFunding)}
                                </button>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </main>
    )
}

export default List