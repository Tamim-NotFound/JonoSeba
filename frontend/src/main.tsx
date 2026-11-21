
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import {
  BrowserRouter,
  Route,
  Routes,
} from "react-router-dom";

import i18n from "./i18n";
import App from "./App";

import { AuthProvider } from "./AuthContext";

import {
  LoginPage,
  RegisterPage,
} from "./AuthPages";

import DashboardPage from "./DashboardPage";

import "./index.css";

// Set the correct document language on startup.
document.documentElement.lang =
  i18n.resolvedLanguage === "en" ? "en" : "bn";

const rootElement = document.getElementById("root");

if (!rootElement) {
  throw new Error("React root element not found.");
}

createRoot(rootElement).render(
  <StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          {/* Real authentication pages */}
          <Route
            path="/login"
            element={<LoginPage />}
          />

          <Route
            path="/register"
            element={<RegisterPage />}
          />

          {/* Protected citizen dashboard */}
          <Route
            path="/dashboard"
            element={<DashboardPage view="home" />}
          />

          {/* Complaint draft form */}
          <Route
            path="/dashboard/complaints/new"
            element={<DashboardPage view="new" />}
          />

          {/* Complaint tracking */}
          <Route
            path="/dashboard/complaints/track"
            element={<DashboardPage view="track" />}
          />

          {/* Citizen complaint list */}
          <Route
            path="/dashboard/complaints"
            element={<DashboardPage view="complaints" />}
          />

          {/* Citizen profile */}
          <Route
            path="/dashboard/profile"
            element={<DashboardPage view="profile" />}
          />

          {/* Existing public website */}
          <Route
            path="/*"
            element={<App />}
          />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  </StrictMode>,
);
