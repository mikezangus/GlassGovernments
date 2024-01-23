import React from "react";
import "../../css/header.css";


export default function RenderHeader() {
    return (
        <div className="header">
            <div className="title">
                Glass Governments
            </div>
            <div className="links">
                <a
                    href="https://github.com/mikezangus/GlassGovernments"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    Github
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