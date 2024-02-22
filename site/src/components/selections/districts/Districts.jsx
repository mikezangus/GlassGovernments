import { useState } from "react";
import useFetchDistricts from "./useFetchDistricts";
import RenderDistricts from "./RenderDistricts";


export default function Districts({ year, office, state, selectedDistrict, onDistrictSelect }) {

    const [districts, setDistricts] = useState([]);
    const [isOpen, setIsOpen] = useState(false);

    useFetchDistricts(year, office, state, setDistricts);

    const toggleDropdown = () => setIsOpen(!isOpen);
    const handleDistrictClick = (district) => {
        onDistrictSelect(district);
        setIsOpen(false);
    };

    return (
        <RenderDistricts
            districts={districts}
            selectedDistrict={selectedDistrict}
            isOpen={isOpen}
            toggleDropdown={toggleDropdown}
            handleDistrictClick={handleDistrictClick}
        />
    );
    
};