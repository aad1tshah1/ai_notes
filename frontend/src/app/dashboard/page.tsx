import { Button } from "@/components/Button";
import { Card } from "@/components/Card";

export default function DashboardPage() {
  return (
    <main className="min-h-screen bg-[#F5F5F7] px-6 py-10 text-[#1D1D1F]">
      <section className="mx-auto max-w-5xl">
        <header className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-[#6E6E73]">AI Notes</p>
            <h1 className="mt-2 text-4xl font-semibold tracking-tight">
              Your notes
            </h1>
          </div>

          <Button>Upload audio</Button>
        </header>

        <div className="mt-10 grid gap-4">
          <Card>
            <p className="text-sm font-medium text-[#6E6E73]">
              No notes yet
            </p>
            <h2 className="mt-2 text-2xl font-semibold">
              Upload your first meeting recording
            </h2>
            <p className="mt-3 max-w-xl text-sm leading-6 text-[#6E6E73]">
              AI Notes will transcribe your audio, summarise the discussion,
              and extract key points and action items.
            </p>
          </Card>
        </div>
      </section>
    </main>
  );
}