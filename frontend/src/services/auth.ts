import { API_URL } from "@/lib/api";

type RegisterPayload = {
  email: string;
  password: string;
};

type LoginPayload = {
  email: string;
  password: string;
};

export async function registerUser(payload: RegisterPayload) {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error("Failed to register");
  }

  return response.json();
}

export async function loginUser(payload: LoginPayload) {
  const formData = new URLSearchParams();

  formData.append("username", payload.email);
  formData.append("password", payload.password);

  const response = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Invalid email or password");
  }

  return response.json();
}