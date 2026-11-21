
import React, { type ReactNode } from "react";
import ReactDOM from "react-dom/client";

import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import "./i18n";
import "./index.css";

import App from "./App";

import {
  LoginPage,
  RegisterPage,
} from "./AuthPages";

import {
  AuthProvider,
  useAuth,
} from "./AuthContext";

import DashboardPage from "./DashboardPage";
import AdminPage from "./AdminPage";

/*
  Citizen dashboard guard.

  Logged-out users go to Login.
  Admin users go to Admin Dashboard.
  Citizens can access their own dashboard.
*/
function CitizenRoute({
  children,
}: {
  children: ReactNode;
}) {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div role="status">
        Loading JonoSeba...
      </div>
    );
  }

  if (!user) {
    return (
      <Navigate to="/login" replace />
    );
  }

  if (user.role === "admin") {
    return (
      <Navigate to="/admin" replace />
    );
  }

  return <>{children}</>;
}

/*
  Current login page redirects to /dashboard.

  CitizenRoute automatically redirects
  admin accounts from /dashboard to /admin.

  This preserves the existing login form.
*/

ReactDOM.createRoot(
  document.getElementById("root")!,
).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route
            path="/login"
            element={<LoginPage />}
          />

          <Route
            path="/register"
            element={<RegisterPage />}
          />

          <Route
            path="/dashboard"
            element={
              <CitizenRoute>
                <DashboardPage view="home" />
              </CitizenRoute>
            }
          />

          <Route
            path="/dashboard/complaints/new"
            element={
              <CitizenRoute>
                <DashboardPage view="new" />
              </CitizenRoute>
            }
          />

          <Route
            path="/dashboard/complaints/track"
            element={
              <CitizenRoute>
                <DashboardPage view="track" />
              </CitizenRoute>
            }
          />

          <Route
            path="/dashboard/complaints"
            element={
              <CitizenRoute>
                <DashboardPage view="complaints" />
              </CitizenRoute>
            }
          />

          <Route
            path="/dashboard/profile"
            element={
              <CitizenRoute>
                <DashboardPage view="profile" />
              </CitizenRoute>
            }
          />

          <Route
            path="/admin"
            element={<AdminPage />}
          />

          <Route
            path="/*"
            element={<App />}
          />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>,
);
