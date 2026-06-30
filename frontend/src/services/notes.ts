import { apiFetch } from "@/lib/api";

export async function getNotes() {
  return apiFetch("/notes");
}