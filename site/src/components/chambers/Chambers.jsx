import { useState } from "react";
import useFetchChambers from "./ChambersFetcher";
import ChambersSwitch from "./ChamberSelector";


export default function SelectChamber({ onChamberSelect }) {

    const [chambers, setChambers] = useState([]);
    const [defaultChamber, setDefaultChamber] = useState(null);

    useFetchChambers(setChambers, setDefaultChamber, onChamberSelect);

    const handleChamberClick = (chamber) => {
        setDefaultChamber(chamber);
        onChamberSelect(chamber);
    };

    return ChambersSwitch(chambers, defaultChamber, handleChamberClick);

};