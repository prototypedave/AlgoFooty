export default function HomeLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="text-white">
        <main>{children}</main>
      </body>
    </html>
  )
}