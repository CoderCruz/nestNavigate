
import { useEffect, useState } from "react";
import axios from "axios";

export default function Dashboard({ onLogout }) {
  const [user, setUser] = useState(null);
  const [modules, setModules] = useState([]);
  const [loading, setLoading] = useState(true);

  const token = localStorage.getItem("token");

  useEffect(() => {
    if (!token) {
      onLogout();
      return;
    }

    const fetchData = async () => {
      try {
        const [profileRes, modulesRes] = await Promise.all([
          axios.get("http://localhost:8000/api/users/profile", {
            headers: { Authorization: `Bearer ${token}` },
          }),
          axios.get("http://localhost:8000/api/modules", {
            headers: { Authorization: `Bearer ${token}` },
          }),
        ]);

        setUser(profileRes.data);
        setModules(modulesRes.data);
      } catch (err) {
        console.error(err);
        onLogout();
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [token, onLogout]);

  if (loading) return <div className="text-white">Loading...</div>;
  if (!user) return <div className="text-red-500">Error loading profile</div>;

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Welcome, {user.name}</h1>
        <button
          onClick={() => {
            localStorage.removeItem("token");
            onLogout();
          }}
          className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded"
        >
          Logout
        </button>
      </div>

      <div className="bg-gray-800 p-4 rounded shadow-lg mb-6">
        <p className="text-lg">💰 Coins Earned: {user.coins_earned}</p>
      </div>

      <h2 className="text-xl font-bold mb-4">Learning Modules</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {modules.map((module) => (
          <div
            key={module.id}
            className="bg-gray-800 p-4 rounded shadow hover:shadow-lg transition"
          >
            <h3 className="text-lg font-semibold">{module.title}</h3>
            <p className="text-sm text-gray-400">{module.difficulty}</p>
            <p className="mt-2">Total Coins: {module.total_coins}</p>

            <div className="mt-3 w-full bg-gray-700 rounded-full h-2">
              <div
                className="bg-blue-500 h-2 rounded-full"
                style={{ width: "0%" }}>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

