
import { useEffect, useState } from "react";
import axios from "axios";

interface User {
  id: number;
  name: string;
  email: string;
  coins_earned: number;
}

interface Module {
  id: string;
  title: string;
  total_coins: number;
  difficulty: string;
}

interface Progress {
  module_id: string;
  completion_percentage: number;
  last_accessed: string;
}

interface DashboardProps {
  onLogout: () => void;
}

export default function Dashboard({ onLogout }: DashboardProps) {
  const [user, setUser] = useState<User | null>(null);
  const [modules, setModules] = useState<Module[]>([]);
  const [progress, setProgress] = useState<Progress[]>([]);
  const [loading, setLoading] = useState(true);

  const token = localStorage.getItem("token");

  useEffect(() => {
    if (!token) {
      onLogout();
      return;
    }

    const fetchData = async () => {
      try {
        const profileRes = await axios.get<User>("http://localhost:8000/api/users/profile", {
          headers: { Authorization: `Bearer ${token}` },
        });

        const modulesRes = await axios.get<Module[]>("http://localhost:8000/api/modules", {
          headers: { Authorization: `Bearer ${token}` },
        });

        const progressRes = await axios.get<Progress[]>(
          `http://localhost:8000/api/users/progress/${profileRes.data.id}`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );

        setUser(profileRes.data);
        setModules(modulesRes.data);
        setProgress(progressRes.data);
      } catch (err) {
        console.error(err);
        onLogout();
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [token, onLogout]);

  const completeLesson = async (moduleId: string, lessonName: string) => {
    try {
      const res = await axios.post(
        "http://localhost:8000/api/progress/complete-lesson",
        { module_id: moduleId, lesson_name: lessonName },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setUser((prev) =>
        prev ? { ...prev, coins_earned: res.data.user.coins_earned } : prev
      );
      setProgress(res.data.progress);
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) return <div className="text-white">Loading...</div>;
  if (!user) return <div className="text-red-500">Error loading profile</div>;

  const getCompletion = (moduleId: string) => {
    const modProgress = progress.find((p) => p.module_id === moduleId);
    return modProgress ? modProgress.completion_percentage : 0;
  };

  const getCompletedLessons = (moduleId: string) => {
    const modProgress = progress.find((p) => p.module_id === moduleId);
    return modProgress ? modProgress.lessons_completed : [];
  };

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
        <p className="text-lg">Coins Earned: {user.coins_earned}</p>
      </div>

      <h2 className="text-xl font-bold mb-4">Learning Modules</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {modules.map((module) => {
          const completion = getCompletion(module.id);
          const completedLessons = getCompletedLessons(module.id);

          return (
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
                  style={{ width: `${completion}%` }}
                ></div>
              </div>
              <p className="text-sm mt-1">{completion}% completed</p>

              <div className="mt-4">
                {module.lessons.split(",").map((lesson) => {
                  const isCompleted = completedLessons.includes(lesson.trim());
                  return (
                    <button
                      key={lesson}
                      onClick={() => completeLesson(module.id, lesson.trim())}
                      disabled={isCompleted}
                      className={`mt-2 px-3 py-1 rounded text-sm block w-full ${
                        isCompleted
                          ? "bg-gray-500 cursor-not-allowed"
                          : "bg-green-600 hover:bg-green-700"
                      }`}
                    >
                      {isCompleted ? `${lesson} Completed` : `Complete ${lesson}`}
                    </button>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

