import { Button } from "@/components/Button";
import { Card } from "@/components/Card";
import { Input } from "@/components/Input";

export default function RegisterPage() {
  return (
    <main className="min-h-screen bg-[#F5F5F7] px-6 text-[#1D1D1F]">
      <section className="mx-auto flex min-h-screen max-w-md flex-col justify-center">
        <div className="mb-8 text-center">
          <p className="text-sm font-medium text-[#6E6E73]">AI Notes</p>
          <h1 className="mt-3 text-4xl font-semibold tracking-tight">
            Create your account
          </h1>
          <p className="mt-3 text-sm leading-6 text-[#6E6E73]">
            Start turning your meeting recordings into structured notes.
          </p>
        </div>

        <Card>
          <form className="space-y-5">
            <Input label="Email" type="email" placeholder="you@example.com" />
            <Input label="Password" type="password" placeholder="••••••••" />

            <Button>Create account</Button>
          </form>
        </Card>
      </section>
    </main>
  );
}