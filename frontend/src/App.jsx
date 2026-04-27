import { useEffect, useState } from "react";
import { AlertPanel } from "./components/AlertPanel";
import { ControlPanel } from "./components/ControlPanel";
import { HeatmapPanel } from "./components/HeatmapPanel";
import { LoginPanel } from "./components/LoginPanel";
import { SummaryCards } from "./components/SummaryCards";
import { fetchAlerts, fetchHeatmap, login, openAlertsSocket, startDemoStream } from "./services/api";

export default function App() {
  const [alerts, setAlerts] = useState([]);
  const [heatmap, setHeatmap] = useState([]);
  const [isAuthenticated, setIsAuthenticated] = useState(Boolean(localStorage.getItem("crowd_guard_token")));
  const [authError, setAuthError] = useState("");
  const [panelError, setPanelError] = useState("");
  const [loadingLogin, setLoadingLogin] = useState(false);
  const [startingStream, setStartingStream] = useState(false);
  const [sourceStatus, setSourceStatus] = useState("Awaiting activation");

  useEffect(() => {
    if (!isAuthenticated) {
      return undefined;
    }

    let active = true;

    async function loadDashboard() {
      try {
        const [alertsData, heatmapData] = await Promise.all([fetchAlerts(), fetchHeatmap()]);
        if (!active) {
          return;
        }
        setAlerts(alertsData.items ?? []);
        setHeatmap(heatmapData.points ?? []);
      } catch (error) {
        setPanelError(error?.response?.data?.detail ?? "Unable to load dashboard data.");
      }
    }

    loadDashboard();

    const interval = window.setInterval(async () => {
      try {
        const [alertsData, heatmapData] = await Promise.all([fetchAlerts(), fetchHeatmap()]);
        if (active) {
          setAlerts(alertsData.items ?? []);
          setHeatmap(heatmapData.points ?? []);
        }
      } catch {
        if (active) {
          setPanelError("Live heatmap refresh failed.");
        }
      }
    }, 3000);

    const socket = openAlertsSocket((message) => {
      if (message.event === "alert.created") {
        setAlerts((current) => [message.data, ...current].slice(0, 20));
        setSourceStatus("Live alerts streaming");
      }
    });

    return () => {
      active = false;
      window.clearInterval(interval);
      socket.close();
    };
  }, [isAuthenticated]);

  async function handleLogin(username, password) {
    setLoadingLogin(true);
    setAuthError("");
    try {
      await login(username, password);
      setIsAuthenticated(true);
      setSourceStatus("Authority session active");
    } catch (error) {
      setAuthError(error?.response?.data?.detail ?? "Sign in failed.");
    } finally {
      setLoadingLogin(false);
    }
  }

  async function handleStartDemo(profile) {
    setStartingStream(true);
    setPanelError("");
    try {
      await startDemoStream(profile);
      setSourceStatus("Demo stream running");
    } catch (error) {
      setPanelError(error?.response?.data?.detail ?? "Unable to start demo monitoring.");
    } finally {
      setStartingStream(false);
    }
  }

  return (
    <main className="app-shell">
      <section className="hero">
        <div>
          <p className="eyebrow">Crowd Guard</p>
          <h1>AI-powered crowd anomaly response center</h1>
          <p className="subtitle">
            Edge-first detection, privacy-preserving analytics, live heatmaps,
            and tamper-evident tourist identity verification.
          </p>
        </div>
      </section>

      {!isAuthenticated ? (
        <LoginPanel onLogin={handleLogin} loading={loadingLogin} error={authError} />
      ) : null}

      <SummaryCards alerts={alerts} />

      <section className="grid">
        <HeatmapPanel points={heatmap} />
        <AlertPanel alerts={alerts} />
      </section>

      {isAuthenticated ? (
        <section className="grid secondary-grid">
          <ControlPanel
            onStartDemo={handleStartDemo}
            starting={startingStream}
            sourceStatus={sourceStatus}
            error={panelError}
          />
          <section className="panel">
            <div className="panel-header">
              <h2>System Status</h2>
              <span>Backend-driven UI</span>
            </div>
            <p className="helper-text">
              This dashboard does not perform detection itself. It visualizes alerts and heatmap
              data produced by the backend AI pipeline and WebSocket stream.
            </p>
          </section>
        </section>
      ) : null}
    </main>
  );
}
