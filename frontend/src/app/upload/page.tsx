"use client";

import { useRef, useState } from "react";

import { Card } from "@/components/Card";
import { Button } from "@/components/Button";
import { useRouter } from "next/navigation";
import { createNote } from "@/services/notes";

export default function UploadPage() {
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const router = useRouter();
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState("");

  function openFilePicker() {
    fileInputRef.current?.click();
  }

  function handleFileChange(event: React.ChangeEvent<HTMLInputElement>) {
    const selectedFile = event.target.files?.[0];

    if (!selectedFile) {
      return;
    }

    setFile(selectedFile);
  }

  async function handleUpload() {
    if (!file) return;

    setIsUploading(true);
    setError("");

    try {
        const data = await createNote(file);
        router.push(`/jobs/${data.job_id}`);
    } catch {
        setError("Failed to upload audio. Please try again.");
    } finally {
        setIsUploading(false);
    }
    }

  return (
    <main className="flex min-h-screen items-center justify-center bg-[#F5F5F7] px-6 text-[#1D1D1F]">
      <section className="w-full max-w-2xl">
        <div className="mb-10 text-center">
          <p className="text-sm font-medium text-[#6E6E73]">AI Notes</p>

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
            <input
              ref={fileInputRef}
              type="file"
              accept="audio/*"
              onChange={handleFileChange}
              className="hidden"
            />

            <div className="mb-8 flex h-20 w-20 items-center justify-center rounded-3xl bg-[#F5F5F7] text-4xl">
              {file ? "🎵" : "🎙️"}
            </div>

            {file ? (
              <>
                <h2 className="text-3xl font-semibold tracking-tight">
                  {file.name}
                </h2>

                <p className="mt-4 text-sm leading-7 text-[#6E6E73]">
                  {(file.size / 1024 / 1024).toFixed(2)} MB · Ready to upload
                </p>

                <div className="mt-10 flex gap-3">
                <Button onClick={openFilePicker} variant="secondary">
                    Choose another
                </Button>

                <Button onClick={handleUpload}>
                    {isUploading ? "Uploading..." : "Upload"}
                </Button>
                </div>

                {error && (
                <p className="mt-4 text-sm text-red-500">
                    {error}
                </p>
                )}
              </>
            ) : (
              <>
                <h2 className="text-3xl font-semibold tracking-tight">
                  Select an audio file
                </h2>

                <p className="mt-4 max-w-md text-sm leading-7 text-[#6E6E73]">
                  MP3, WAV and M4A recordings are supported.
                </p>

                <div className="mt-10">
                  <Button onClick={openFilePicker}>Choose file</Button>
                </div>
              </>
            )}
          </div>
        </Card>
      </section>
    </main>
  );
}