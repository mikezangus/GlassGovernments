import { useState } from "react";
import useFetchOffices from "./useFetchOffices";
import RenderOffices from "./RenderOffices";


export default function ShowOffices({ year, onOfficeSelect }) {

    const [offices, setOffices] = useState([]);
    const [defaultOffice, setDefaultOffice] = useState(null);

    useFetchOffices(year, setOffices, setDefaultOffice, onOfficeSelect);

    const handleOfficeClick = (office) => {
        setDefaultOffice(office);
        onOfficeSelect(office);
    };

    return (
        <RenderOffices
            offices={offices}
            defaultOffice={defaultOffice}
            handleOfficeClick={handleOfficeClick}
        />
    );

};