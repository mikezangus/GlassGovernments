// "use client";


// import { useEffect, useState } from "react";


// const URL_BASE = "http://localhost:3001/api/";


// async function fetchCongresses(): Promise<number[]>
// {
//     try {
//         const res = await fetch(`${URL_BASE}congresses`);
//         const data = await res.json();
//         return data.map((row: {congress: number }) => row.congress);
//     } catch (err) {
//         console.error("Failed to fatch congresses:", err);
//         return [];
//     }
// }


// async function fetchBillTypes(congress: number): Promise<string[]>
// {
//     try {
//         const res = await fetch(`${URL_BASE}bill-types?congress=${congress}`);
//         const data = await res.json();
//         return data.map((row: { type: string }) => row.type);
//     } catch (err) {
//         console.error("Failed to fetch bill types:", err);
//         return [];
//     }
// }


// async function fetchBillNums(congress: number, billType: string): Promise<number[]>
// {
//     try {
//         const res = await fetch(`${URL_BASE}bill-nums?congress=${congress}&bill-type=${billType}`);
//         const data = await res.json();
//         return data.map((row: { bill_num: number }) => row.bill_num);
//     } catch (err) {
//         console.error("Failed to fetch bill types:", err);
//         return [];
//     }
// }


// function CongressesComponent({ onSelect }:
//                              { onSelect: (congress: number) => void })
// {
//     const [congresses, setCongresses] = useState<number[]>([]);
//     useEffect(() => {
//         const load = async () => {
//             const results = await fetchCongresses();
//             setCongresses(results);
//         };
//         load();
//     }, []);
//     return (
//         <div>
//             <h2>Congresses</h2>
//             <ul>
//                 {congresses.map((item) => (
//                     <li
//                         key={item}
//                         style={{ cursor: "pointer" }}
//                         onClick={() => onSelect(item)}
//                     >
//                         {item}
//                     </li>
//                 ))}
//             </ul>
//         </div>
//     );
// }


// function BillTypesComponent({ congress,
//                               onSelect }:
//                             { congress: number,
//                               onSelect: (billType: string) => void })
// {
//     const [billTypes, setBillTypes] = useState<string[]>([]);
//     useEffect(() => {
//         const load = async () => {
//             const results = await fetchBillTypes(congress);
//             setBillTypes(results);
//         };
//         if (congress) {
//             load();
//         }
//     }, []);
//     return (
//         <div>
//             <h2>Bill Types</h2>
//             <ul>
//                 {billTypes.map((item) => (
//                     <li
//                         key={item}
//                         style={{ cursor: "pointer" }}
//                         onClick={() => onSelect(item)}
//                     >
//                         {item}
//                     </li>
//                 ))}
//             </ul>
//         </div>
//     );
// }


// function BillNumsComponent({ congress,
//                              billType,
//                              onSelect }:
//                            { congress: number,
//                              billType: string,
//                              onSelect: (billNum: number) => void })
// {
//     const [billNums, setBillNums] = useState<number[]>([]);
//     useEffect(() => {
//         const load = async () => {
//             const results = await fetchBillNums(congress, billType);
//             setBillNums(results);
//         };
//         if (congress && billType) {
//             load();
//         }
//     }, []);
//     return (
//         <div>
//             <h2>Bill Numbers</h2>
//             <ul>
//                 {billNums.map((item) => (
//                     <li
//                         key={item}
//                         style={{ cursor: "pointer" }}
//                         onClick={() => onSelect(item)}
//                     >
//                         {item}
//                     </li>
//                 ))}
//             </ul>
//         </div>
//     );
// }


// export default function BillsComponent()
// {
//     const [selectedCongress, setSelectedCongress] = useState<number | null>(null);
//     const [selectedBillType, setSelectedBillType] = useState<string | null>(null);
//     const [selectedBillNum, setSelectedBillNum] = useState<number | null>(null);
//     return (
//         <main>
//             <h1>Bills</h1>
//             <CongressesComponent onSelect={setSelectedCongress}/>
//             {
//                 selectedCongress
//                 && <BillTypesComponent
//                     congress={selectedCongress}
//                     onSelect={setSelectedBillType}
//                     />
//             }
//             {
//                 selectedCongress
//                 && selectedBillType
//                 && <BillNumsComponent
//                     congress={selectedCongress}
//                     billType={selectedBillType}
//                     onSelect={setSelectedBillNum}
//                     />
//             }
//             {selectedBillNum && <div>{selectedCongress}-{selectedBillType}-{selectedBillNum}</div>}
//         </main>
//     );
// }
