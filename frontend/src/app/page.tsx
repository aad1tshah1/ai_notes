"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

import { Button } from "@/components/Button";
import { Card } from "@/components/Card";
import { Input } from "@/components/Input";
import { loginUser } from "@/services/auth";

export default function LoginPage() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");

    try {
      const data = await loginUser({ email, password });
      localStorage.setItem("access_token", data.access_token);
      router.push("/dashboard");
    } catch {
      setError("Invalid email or password");
    }
  }

  return (
    <main className="min-h-screen bg-[#F5F5F7] px-6 text-[#1D1D1F]">
      <section className="mx-auto flex min-h-screen max-w-md flex-col justify-center">
        <div className="mb-8 text-center">
          <p className="text-sm font-medium text-[#6E6E73]">AI Notes</p>
          <h1 className="mt-3 text-4xl font-semibold tracking-tight">
            Welcome back
          </h1>
          <p className="mt-3 text-sm leading-6 text-[#6E6E73]">
            Sign in to view and create your meeting notes.
          </p>
        </div>

        <Card>
          <form onSubmit={handleSubmit} className="space-y-5">
            <Input
              label="Email"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
            />

            <Input
              label="Password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
            />

            {error && <p className="text-sm text-red-500">{error}</p>}

            <Button>Sign in</Button>
          </form>
        </Card>
      </section>
    </main>
  );
}