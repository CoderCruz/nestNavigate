import { useState } from "react";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";

export default function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));

  return token ? (
    <Dashboard onLogout={() => setToken(null)} />
  ) : (
    <Login onLogin={(newToken) => setToken(newToken)} />
  );
}

