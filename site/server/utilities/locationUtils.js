function haversine(lat1, lon1, lat2, lon2) {
    const R = 3958.8;
    const rlat1 = Math.PI * lat1 / 180;
    const rlat2 = Math.PI * lat2 / 180;
    const difflat = rlat2 - rlat1;
    const difflon = Math.PI * (lon2 - lon1) / 180;
    const d = 2 * R * Math.asin(Math.sqrt(Math.sin(difflat / 2) * Math.sin(difflat / 2) + Math.cos(rlat1) * Math.cos(rlat2) * Math.sin(difflon / 2)));
    return d;
};

function groupCoordinates(coordinates) {
    const groupedCoords = [];
    const threshold = 10;
    coordinates.forEach(coord => {
        let isGrouped = false;
        for (const group of groupedCoords) {
            for (const point of group) {
                if (haversine(coord.latitude, coord.longitude, point.latitude, point.longitude) <= threshold) {
                    group.push(coord);
                    isGrouped = true;
                    break;
                }
            }
            if (isGrouped) break;
        }
        if (!isGrouped) {
            groupedCoords.push([coord]);
        }
    });
    return groupedCoords;
};

module.exports = { haversine, groupCoordinates };