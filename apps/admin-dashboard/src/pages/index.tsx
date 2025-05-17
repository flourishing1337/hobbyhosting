import Head from "next/head";
import Link from "next/link";

export default function Home() {
  return (
    <>
      <Head>
        <title>HobbyHosting Admin</title>
      </Head>
      <main className="p-4">
        <h1 className="text-2xl font-bold mb-4">Admin Dashboard</h1>
        <Link href="/dashboard" className="text-blue-600 underline">
          Go to Dashboard
        </Link>
      </main>
    </>
  );
}
