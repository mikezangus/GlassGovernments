import React from "react";
import Header from "./components/Header";
import DropdownDistricts from "./components/DropdownDistricts";
import DropdownPoliticians from "./components/DropdownPoliticians";

export default function App() {
    return (
        <div className="appContainer">
            <Header />
            <div className="contentContainer">
                <div className="leftHalf">
                    <DropdownDistricts />
                    <DropdownPoliticians />
                </div>
                <div className="rightHalf">

                </div>
            </div>
        </div>
    )
}
