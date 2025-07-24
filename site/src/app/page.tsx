import "../styles/index.css";
import { redirect } from "next/navigation";


export default function Home()
{
    redirect("/bill-tracking");
}
