"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";

import { Card } from "@/components/Card";
import { getJob } from "@/services/jobs";

type Job = {
  job_id: string;
  status: string;
  note_id: string | null;
  error_message: string | null;
};

export default function JobPage() {
  const params = useParams();
  const router = useRouter();

  const jobId = params.job_id as string;

  const [job, setJob] = useState<Job | null>(null);

  useEffect(() => {
    async function checkJob() {
      const data = await getJob(jobId);
      setJob(data);

      if (data.status === "completed" && data.note_id) {
        router.push(`/notes/${data.note_id}`);
      }
    }

    checkJob();

    const interval = setInterval(checkJob, 2000);

    return () => clearInterval(interval);
  }, [jobId, router]);

  const status = job?.status ?? "pending";

  return (
    <main className="flex min-h-screen items-center justify-center bg-[#F5F5F7] px-6 text-[#1D1D1F]">
      <section className="w-full max-w-2xl">
        <Card className="text-center">
          <div className="py-16">
            <div className="mb-6 text-5xl">⏳</div>

            <h1 className="text-3xl font-semibold">
              Processing your meeting
            </h1>

            <p className="mt-4 text-[#6E6E73]">
              Current status: {status}
            </p>

            <div className="mt-8 rounded-xl bg-[#F5F5F7] p-4 text-left">
              <p className="text-xs uppercase text-[#6E6E73]">Job ID</p>
              <p className="mt-2 break-all font-mono text-sm">{jobId}</p>
            </div>
          </div>
        </Card>
      </section>
    </main>
  );
}