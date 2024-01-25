import React from "react";
import "../../css/header.css";


export default function RenderHeader() {
    return (
        <div className="header">
            <div className="title">
                <a href="https://glassgovernments.com">
                    Glass Governments
                </a>
            </div>
            <div className="links">
                <a
                    href="https://glassgovernments.com/about"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    About
                </a>
                <a
                    href="https://google.com"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    Submit feedback
                </a>
            </div>
        </div>
    );
};