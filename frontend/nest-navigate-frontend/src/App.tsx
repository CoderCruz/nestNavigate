import { useState, useEffect } from "react";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import axios from "axios";

export default function App() {
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [loadingAuth, setLoadingAuth] = useState(true);

  axios.defaults.withCredentials = true;

  useEffect(() => {
    const pingBackend = () => {
      axios
        .get(`${API_BASE_URL}/`, { timeout: 3000 })
        .then(() => console.log("Keep-alive ping successful"))
        .catch(() => console.log("Keep-alive ping failed"));
    };
    pingBackend();
    const interval = setInterval(pingBackend, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, [API_BASE_URL]);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const res = await axios.get(`${API_BASE_URL}/api/users/profile`, {
          withCredentials: true,
          timeout: 5000,
        });
        if (res.data?.isLoggedIn === false) {
          setIsLoggedIn(false);
        } else {
          setIsLoggedIn(true);
        }
      } catch (err) {
        console.error("Auth check failed:", err);
        setIsLoggedIn(false);
      } finally {
        setLoadingAuth(false);
      }
    };
    checkAuth();
  }, [API_BASE_URL]);

  const handleLoginSuccess = () => {
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
  };

  if (loadingAuth) {
    return (
      <>
        <div className="text-gray-400 text-center mt-4">
          Checking your session...
        </div>
        <Login onLogin={handleLoginSuccess} />
      </>
    );
  }

  return isLoggedIn ? (
    <Dashboard onLogout={handleLogout} />
  ) : (
    <Login onLogin={handleLoginSuccess} />
  );
}

