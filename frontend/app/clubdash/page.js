import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export default async function Page() {
  const data = await fetch("http://127.0.0.1:8000/bins");
  const clubs = await data.json();
  console.log(clubs);
  return (
    <div className="font-sans p-8 pb-20 gap-16 sm:p-20">
      <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
        <h1 className="text-6xl">Updations</h1>
      </main>
    </div>
  );
}
