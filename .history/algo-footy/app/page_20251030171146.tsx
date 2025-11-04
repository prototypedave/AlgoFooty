import HomePage from "@/app/home/page"

export default function App() {
    const content = HomePage()
    return (
      <div>
        {content}
      </div>
    )
}