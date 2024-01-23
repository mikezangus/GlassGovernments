import { useState } from "react";
import useFetchChambers from "./useFetchChambers";
import RenderChambers from "./RenderChambers";


export default function ShowChambers({ onChamberSelect }) {

    const [chambers, setChambers] = useState([]);
    const [defaultChamber, setDefaultChamber] = useState(null);

    useFetchChambers(setChambers, setDefaultChamber, onChamberSelect);

    const handleChamberClick = (chamber) => {
        setDefaultChamber(chamber);
        onChamberSelect(chamber);
    };

    return (
        <RenderChambers
            chambers={chambers}
            defaultChamber={defaultChamber}
            handleChamberClick={handleChamberClick}
        />
    );

};