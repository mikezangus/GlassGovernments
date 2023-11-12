import React, { useState } from "react";
import Header from "./components/Header";
import DropdownDistricts from "./components/DropdownDistricts";
import DropdownPoliticians from "./components/DropdownPoliticians";

export default function App() {
    const [selectedDistrict, setSelectedDistrict] = useState(null);
    const handleSelectDistrict = (districtData) => {
        setSelectedDistrict(districtData);
    };
    return (
        <div className="appContainer">
            <Header />
            <DropdownDistricts onSelectedDistrict={handleSelectDistrict} />
            {selectedDistrict ? (
                <DropdownPoliticians district={selectedDistrict}/>
            ) : null }
        </div>
    );
};
