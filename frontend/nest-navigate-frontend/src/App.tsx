import { useState } from "react";
import Login from "./pages/Login";

export default function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));

  return token ? (
    <div className="h-screen flex items-center justify-center bg-green-900 text-white">
      <h1>Dashboard (Token Stored)</h1>
    </div>
  ) : (
    <Login onLogin={(token) => setToken(token)} />
  );
}
