import { apiFetch } from "@/lib/api";
import type { Note } from "@/types/note";

type CreateNoteResponse = {
  job_id: string;
  status: string;
  message: string;
};

export async function getNotes(): Promise<Note[]> {
  return apiFetch("/notes");
}

export async function createNote(file: File): Promise<CreateNoteResponse> {
  const formData = new FormData();
  formData.append("audio_file", file);

  return apiFetch("/notes", {
    method: "POST",
    body: formData,
  });
}

export async function getNote(noteId: string): Promise<Note> {
  return apiFetch(`/notes/${noteId}`);
}