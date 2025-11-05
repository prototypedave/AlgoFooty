import Image from "next/image";

export default function Home() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-oxford-blue font-sans">
        <main className="flex flex-col pr-50 gap-16">
            <h1 className="text-9xl font-bold">GET IN TOUCH</h1>
            <div className="text-4xl flex justify-between">
              <div className="flex flex-col gap-4">
                <p>Popup Sure Predicts</p>
                <p>@popup_sure_predicts</p>
                <p>@popup_sure_predicts</p>
              </div>
              <div className="flex flex-col gap-4">
                <p>+2547123456789</p>
                <p>popupgfj@gmail.com</p>
              </div>
            </div>
        </main>
    </div>
  );
}
