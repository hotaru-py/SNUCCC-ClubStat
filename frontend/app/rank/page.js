import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

export default async function Page() {
  const data = await fetch("http://127.0.0.1:8000/ranked");
  const clubs = await data.json();
  console.log(clubs);
  return (
    <div className="font-sans p-8 pb-20 gap-16 sm:p-20">
      <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
        <h1 className="text-6xl">Club Ranking</h1>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Rank</TableHead>
              <TableHead>Name</TableHead>
              <TableHead>Tags</TableHead>
              <TableHead>Instagram ID</TableHead>
              <TableHead>Community</TableHead>
              <TableHead>Social</TableHead>
              <TableHead>Event</TableHead>
              <TableHead>Collab</TableHead>
              <TableHead>Rating</TableHead>
              <TableHead>Overall Score</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {clubs.map((item, index) => (
              <TableRow key={index}>
                <TableCell>{index + 1}</TableCell>
                <TableCell>{item.name}</TableCell>
                <TableCell>{item.tags}</TableCell>
                <TableCell>{item.insta}</TableCell>
                <TableCell>{item.community}</TableCell>
                <TableCell>{item.social}</TableCell>
                <TableCell>{item.events}</TableCell>
                <TableCell>{item.collab}</TableCell>
                <TableCell>{item.votes}</TableCell>
                <TableCell>{item.overall}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </main>
    </div>
  );
}
