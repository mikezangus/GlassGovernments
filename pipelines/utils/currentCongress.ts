const y2c = require("../../data/years-congresses.json");

console.log("hi")
const currentCongress = () => {
    return y2c[String(new Date().getFullYear())];
}


export default currentCongress;
