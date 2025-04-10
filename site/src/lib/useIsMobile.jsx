import {useEffect, useState} from "react";


export default function useIsMobile() {
    const [isMobile, setIsMobile] = useState(
        window.innerWidth < 820
    );
    useEffect(() => {
        const handleResize = () => {
            setIsMobile(
                window.innerWidth < 820
            )
        };
        window.addEventListener(
            "resize",
            handleResize
        );
        return () => {
            window.removeEventListener(
                "resize",
                handleResize
            )
        };
    }, []);
    return isMobile;
};
