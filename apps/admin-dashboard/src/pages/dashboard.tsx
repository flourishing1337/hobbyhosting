import Head from "next/head";
import { Button } from "../../../packages/ui/src";

export default function Dashboard() {
  return (
    <>
      <Head>
        <title>Dashboard</title>
      </Head>
      <main className="p-4">
        <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
        <Button>Example Button</Button>
      </main>
    </>
  );
}
