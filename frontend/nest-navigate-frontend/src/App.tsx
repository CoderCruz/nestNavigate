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
        } else {
          setIsLoggedIn(false);
        }
      } catch (err: unknown) {
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
    return <div className="text-white">Loading...</div>;
  }

  return isLoggedIn ? (
    <Dashboard onLogout={handleLogout} />
  ) : (
    <Login onLogin={handleLoginSuccess} />
  );
}

