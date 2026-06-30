import { apiFetch } from "@/lib/api";

export async function getJob(jobId: string) {
  return apiFetch(`/jobs/${jobId}`);
}