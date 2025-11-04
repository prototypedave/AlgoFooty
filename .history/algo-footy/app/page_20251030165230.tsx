import HomePage from "@/home_page/page"

export default function App() {
    const content = HomePage()
    return (
      <div>
        {content}
      </div>
    )
}