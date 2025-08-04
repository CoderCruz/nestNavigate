import { useState } from "react";
import axios from "axios";

interface LoginProps {
  onLogin: () => void;
}

export default function Login({ onLogin }: LoginProps) {
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
  const [email, setEmail] = useState<string>("");
  const [name, setName] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [error, setError] = useState<string>("");
  const [isRegister, setIsRegister] = useState<boolean>(false);

  axios.defaults.withCredentials = true;

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");

    try {
      if (isRegister) {
        await axios.post(
          `${API_BASE_URL}/api/users/register`,
          { email, name, password },
          { withCredentials: true }
        );
      }

      const formData = new URLSearchParams();
      formData.append("username", email); 
      formData.append("password", password);

      await axios.post(`${API_BASE_URL}/api/users/login`, formData, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        withCredentials: true,
      });

      const profileRes = await axios.get(`${API_BASE_URL}/api/users/profile`, {
        withCredentials: true,
      });

      if (profileRes.status === 200) {
        onLogin();
      } else {
        setError("Login failed. Please try again.");
      }
    } catch (err: any) {
      if (axios.isAxiosError(err) && err.response?.status === 401) {
        setError("Invalid email or password.");
      } else {
        console.error("Login/Register error:", err);
        setError("Something went wrong. Please try again.");
      }
    }
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gray-900">
      <form
        onSubmit={handleSubmit}
        className="bg-gray-800 p-6 rounded-lg shadow-lg w-96"
      >
        <h2 className="text-2xl font-bold text-white mb-4">
          {isRegister ? "Register" : "Login"}
        </h2>

        {error && <p className="text-red-500 mb-3">{error}</p>}

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full p-2 mb-3 rounded bg-gray-700 text-white"
          required
        />

        {isRegister && (
          <input
            type="text"
            placeholder="Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full p-2 mb-3 rounded bg-gray-700 text-white"
            required
          />
        )}

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full p-2 mb-3 rounded bg-gray-700 text-white"
          required
        />

        <button
          type="submit"
          className="w-full bg-blue-600 hover:bg-blue-700 p-2 rounded text-white font-bold"
        >
          {isRegister ? "Register" : "Login"}
        </button>

        <p className="text-gray-400 mt-3 text-sm">
          {isRegister ? "Already have an account?" : "Don't have an account?"}{" "}
          <button
            type="button"
            onClick={() => setIsRegister(!isRegister)}
            className="text-blue-400 hover:underline"
          >
            {isRegister ? "Login" : "Register"}
          </button>
        </p>
      </form>
    </div>
  );
}

