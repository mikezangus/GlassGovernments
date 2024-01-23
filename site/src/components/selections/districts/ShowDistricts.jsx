import { useState } from "react";
import useFetchDistricts from "./useFetchDistricts";
import RenderDistricts from "./RenderDistricts";


export default function ShowDistricts({ chamber, state, onDistrictSelect }) {

    const [districts, setDistricts] = useState([]);
    const [selectedDistrict, setSelectedDistrict] = useState(null);
    const [isOpen, setIsOpen] = useState(false);

    useFetchDistricts(chamber, state, setDistricts);

    const toggleDropdown = () => setIsOpen(!isOpen);
    const handleDistrictClick = (district) => {
        onDistrictSelect(district);
        setSelectedDistrict(district);
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