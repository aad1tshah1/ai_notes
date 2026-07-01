"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";

import { Card } from "@/components/Card";
import { Button } from "@/components/Button";
import type { Note } from "@/types/note";
import { deleteNote, getNote } from "@/services/notes";

export default function NotePage() {
  const params = useParams();
  const router = useRouter();

  const noteId = params.note_id as string;

  const [note, setNote] = useState<Note | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    async function loadNote() {
      const data = await getNote(noteId);
      setNote(data);
    }

    loadNote();
  }, [noteId]);

  async function handleDelete() {
    const confirmed = window.confirm("Are you sure you want to delete this note?");

    if (!confirmed) return;

    setIsDeleting(true);

    try {
      await deleteNote(noteId);
      router.push("/dashboard");
    } catch {
      setIsDeleting(false);
      alert("Failed to delete note. Please try again.");
    }
  }

  if (!note) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-[#F5F5F7] text-[#1D1D1F]">
        <p className="text-[#6E6E73]">Loading note...</p>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-[#F5F5F7] px-6 py-10 text-[#1D1D1F]">
      <section className="mx-auto max-w-4xl">
        <div className="flex items-center justify-between">
          <Button variant="secondary" onClick={() => router.push("/dashboard")}>
            Back to notes
          </Button>

          <Button variant="secondary" onClick={handleDelete}>
            {isDeleting ? "Deleting..." : "Delete note"}
          </Button>
        </div>

        <div className="mt-10">
          <p className="text-sm font-medium text-[#6E6E73]">
            {new Date(note.created_at).toLocaleDateString()}
          </p>

          <h1 className="mt-3 text-5xl font-semibold tracking-tight">
            Meeting notes
          </h1>
        </div>

        <div className="mt-10 grid gap-6">
          <Card>
            <h2 className="text-2xl font-semibold">Summary</h2>
            <p className="mt-4 leading-7 text-[#6E6E73]">
              {note.notes.summary}
            </p>
          </Card>

          <Card>
            <h2 className="text-2xl font-semibold">Key points</h2>
            <ul className="mt-4 space-y-3 text-[#6E6E73]">
              {note.notes.key_points.map((point, index) => (
                <li key={index}>• {point}</li>
              ))}
            </ul>
          </Card>

          <Card>
            <h2 className="text-2xl font-semibold">Action items</h2>
            {note.notes.action_items.length === 0 ? (
              <p className="mt-4 text-[#6E6E73]">No action items found.</p>
            ) : (
              <ul className="mt-4 space-y-3 text-[#6E6E73]">
                {note.notes.action_items.map((item, index) => (
                  <li key={index}>□ {item}</li>
                ))}
              </ul>
            )}
          </Card>

          <Card>
            <h2 className="text-2xl font-semibold">Transcript</h2>
            <p className="mt-4 whitespace-pre-wrap leading-7 text-[#6E6E73]">
              {note.transcript}
            </p>
          </Card>
        </div>
      </section>
    </main>
  );
}