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
    const checkAuth = async () => {
      try {
        const res = await axios.get(`${API_BASE_URL}/api/users/profile`, {
          withCredentials: true,
        });
        if (res.status === 200) {
          setIsLoggedIn(true);
        }
      } catch (err) {
        if (!(axios.isAxiosError(err) && err.response?.status === 401)) {
          console.error("Auth check failed:", err);
        }
        setIsLoggedIn(false);
      } finally {
        setLoadingAuth(false);
      }
    };

    if (document.cookie.includes("access_token")) {
      checkAuth();
    } else {
      setLoadingAuth(false);
    }
  }, [API_BASE_URL]);

  const handleLoginSuccess = async () => {
    try {
      const res = await axios.get(`${API_BASE_URL}/api/users/profile`, {
        withCredentials: true,
      });
      if (res.status === 200) {
        setIsLoggedIn(true);
      }
    } catch (err) {
      console.error("Post-login profile check failed:", err);
    }
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
  };

  if (loadingAuth) {
    return <div className="text-white">Loading...</div>;
  }

  return isLoggedIn ? (
    <Dashboard onLogout={handleLogout} />
  ) : (
    <Login onLogin={handleLoginSuccess} />
  );
}

