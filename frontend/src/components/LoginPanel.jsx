import { useState } from "react";

export function LoginPanel({ onLogin, loading, error }) {
  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("crowdguard123");

  return (
    <section className="panel auth-panel">
      <div className="panel-header">
        <h2>Authority Login</h2>
        <span>Prototype credentials prefilled</span>
      </div>
      <label className="field">
        <span>Username</span>
        <input value={username} onChange={(event) => setUsername(event.target.value)} />
      </label>
      <label className="field">
        <span>Password</span>
        <input
          type="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
        />
      </label>
      {error ? <p className="error-text">{error}</p> : null}
      <button className="primary-btn" onClick={() => onLogin(username, password)} disabled={loading}>
        {loading ? "Signing in..." : "Sign In"}
      </button>
    </section>
  );
}
