"use client";

import { Card } from "@/components/Card";
import { Button } from "@/components/Button";

export default function UploadPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-[#F5F5F7] px-6 text-[#1D1D1F]">
      <section className="w-full max-w-2xl">
        <div className="mb-10 text-center">
          <p className="text-sm font-medium text-[#6E6E73]">
            AI Notes
          </p>

          <h1 className="mt-3 text-5xl font-semibold tracking-tight">
            Upload audio
          </h1>

          <p className="mt-4 text-base leading-7 text-[#6E6E73]">
            Choose a meeting recording and AI Notes will process it in the
            background.
          </p>
        </div>

        <Card className="text-center">
          <div className="flex min-h-[340px] flex-col items-center justify-center">
            <div className="mb-8 flex h-20 w-20 items-center justify-center rounded-3xl bg-[#F5F5F7] text-4xl">
              🎙️
            </div>

            <h2 className="text-3xl font-semibold tracking-tight">
              Select an audio file
            </h2>

            <p className="mt-4 max-w-md text-sm leading-7 text-[#6E6E73]">
              MP3, WAV and M4A recordings are supported.
            </p>

            <div className="mt-10">
              <Button>Choose file</Button>
            </div>
          </div>
        </Card>
      </section>
    </main>
  );
}