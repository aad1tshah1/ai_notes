"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { Button } from "@/components/Button";
import { Card } from "@/components/Card";
import { getNotes } from "@/services/notes";
import type { Note } from "@/types/note";

export default function DashboardPage() {
  const [notes, setNotes] = useState<Note[]>([]);
  const router = useRouter();

  function goToUpload() {
    router.push("/upload");
  }

  useEffect(() => {
    async function loadNotes() {
      try {
        const data = await getNotes();
        setNotes(data);
      } catch {
        localStorage.removeItem("access_token");
        router.push("/login");
      }
    }

    loadNotes();
  }, [router]);

  return (
    <main className="min-h-screen bg-[#F5F5F7] px-6 py-10 text-[#1D1D1F]">
      <section className="mx-auto max-w-6xl">
        <header className="flex items-start justify-between">
          <div>
            <p className="text-sm font-medium text-[#6E6E73]">
              AI Notes
            </p>

            <h1 className="mt-2 text-5xl font-semibold tracking-tight">
              Your notes
            </h1>

            <p className="mt-4 max-w-xl text-base leading-7 text-[#6E6E73]">
              Upload a meeting recording and AI Notes will turn it into a clear
              summary, key points, and action items.
            </p>
          </div>

          <Button onClick={goToUpload}>
            Upload audio
          </Button>
        </header>

        <section className="mt-12">
          {notes.length === 0 ? (
            <Card className="flex min-h-[320px] flex-col items-center justify-center text-center">
              <div className="mb-6 flex h-16 w-16 items-center justify-center rounded-3xl bg-[#F5F5F7] text-3xl">
                🎙️
              </div>

              <p className="text-sm font-medium text-[#6E6E73]">
                No notes yet
              </p>

              <h2 className="mt-3 max-w-md text-3xl font-semibold tracking-tight">
                Upload your first meeting recording
              </h2>

              <p className="mt-4 max-w-md text-sm leading-6 text-[#6E6E73]">
                Your generated notes will appear here once processing is
                complete.
              </p>

              <div className="mt-8">
                <Button onClick={goToUpload}>
                  Upload audio
                </Button>
              </div>
            </Card>
          ) : (
            <div className="grid gap-6">
              {notes.map((note) => (
                <Card key={note.note_id}>
                  <p className="text-sm font-medium text-[#6E6E73]">
                    {new Date(note.created_at).toLocaleDateString()}
                  </p>

                  <h2 className="mt-2 text-2xl font-semibold tracking-tight">
                    {note.notes.summary}
                  </h2>

                  <p className="mt-3 text-sm leading-6 text-[#6E6E73]">
                    {note.notes.key_points.length} key points ·{" "}
                    {note.notes.action_items.length} action items
                  </p>
                </Card>
              ))}
            </div>
          )}
        </section>
      </section>
    </main>
  );
}