export default function AppLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-blue">
        <main>{children}</main>
      </body>
    </html>
  )
}