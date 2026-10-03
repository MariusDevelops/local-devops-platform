import { useEffect, useState } from "react";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

function App() {
  const [todos, setTodos] = useState([]);
  const [title, setTitle] = useState("");

  const load = async () => {
    const res = await fetch(`${API}/todos`);
    setTodos(await res.json());
  };

  useEffect(() => {
    load();
  }, []);

  const add = async () => {
    if (!title.trim()) return;
    await fetch(`${API}/todos`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title }),
    });
    setTitle("");
    load();
  };

  const toggle = async (todo) => {
    await fetch(`${API}/todos/${todo.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: todo.title, done: !todo.done }),
    });
    load();
  };

  const remove = async (id) => {
    await fetch(`${API}/todos/${id}`, { method: "DELETE" });
    load();
  };

  return (
    <div style={{ maxWidth: 400, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1>Todos</h1>
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && add()}
        placeholder="New todo"
      />
      <button onClick={add}>Add</button>
      <ul style={{ listStyle: "none", padding: 0 }}>
        {todos.map((t) => (
          <li key={t.id}>
            <input type="checkbox" checked={t.done} onChange={() => toggle(t)} />
            <span style={{ textDecoration: t.done ? "line-through" : "none" }}>
              {" "}{t.title}{" "}
            </span>
            <button onClick={() => remove(t.id)}>x</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App
