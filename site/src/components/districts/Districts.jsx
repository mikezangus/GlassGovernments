import { useState } from "react";
import useFetchDistricts from "./DistrictsFetcher";
import DistrictsDropdown from "./DistrictSelector";


export default function SelectDistrict({ chamber, state, onDistrictSelect }) {

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

    return DistrictsDropdown(districts, selectedDistrict, isOpen, toggleDropdown, handleDistrictClick);
    
};