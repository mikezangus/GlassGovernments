import "../styles/index.css";
import Header from "@/components/Header";


export const metadata = {
    title: "Glass Governments",
    description: ""
};


export default function RootLayout({ children }: { children: React.ReactNode })
{
    return (
        <html lang="en">
            <body>
                <header>
                    <Header />
                </header>
                <main>
                    {children}
                </main>
            </body>
        </html>
    );
}
