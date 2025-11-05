export default function HomeLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="en">
        <body>
            <main>{children}</main>
        </body>
        </html>
    )
}