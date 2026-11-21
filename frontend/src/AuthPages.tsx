import {
  useEffect,
  useState,
  type FormEvent,
  type ReactNode,
} from "react";

import {
  Link,
  NavLink,
  Navigate,
  useLocation,
  useNavigate,
  useSearchParams,
} from "react-router-dom";

import { useTranslation } from "react-i18next";

import {
  ArrowLeft,
  ArrowRight,
  ArrowUpRight,
  Eye,
  EyeOff,
  Landmark,
  Languages,
  LockKeyhole,
  LogOut,
  Mail,
  Menu,
  Moon,
  ShieldCheck,
  Sun,
  UserRound,
  X,
} from "lucide-react";

import {
  changeAppLanguage,
  type AppLanguage,
} from "./i18n";

import {
  registerCitizen,
  ApiError,
} from "./api/auth";

import { useAuth } from "./AuthContext";
import "./auth.css";


type Theme = "light" | "dark";

function useEnglish(): boolean {
  const { i18n } = useTranslation();
  return i18n.resolvedLanguage === "en";
}

function getSavedTheme(): Theme {
  try {
    return localStorage.getItem("jonoseba-theme") === "dark"
      ? "dark"
      : "light";
  } catch {
    return "light";
  }
}


function AuthLayout({
  children,
}: {
  children: ReactNode;
}) {
  const { t, i18n } = useTranslation();
  const { pathname } = useLocation();
  const { user } = useAuth();

  const english = i18n.resolvedLanguage === "en";

  const language: AppLanguage = english ? "en" : "bn";

  const [theme, setTheme] = useState<Theme>(
    getSavedTheme
  );

  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    document.documentElement.style.colorScheme = theme;

    try {
      localStorage.setItem("jonoseba-theme", theme);
    } catch {
      // Theme still works without browser storage.
    }
  }, [theme]);

  useEffect(() => {
    setMenuOpen(false);
  }, [pathname]);

  const navigation = [
    {
      path: "/",
      label: t("navHome"),
      end: true,
    },
    {
      path: "/services",
      label: t("navServices"),
      end: false,
    },
    {
      path: "/how-it-works",
      label: t("navHow"),
      end: true,
    },
    {
      path: "/ai-assistant",
      label: t("navAi"),
      end: true,
    },
    {
      path: "/about",
      label: english ? "About" : "সম্পর্কে",
      end: true,
    },
  ];

  return (
    <div className="auth-screen">

      {/* Same navigation design as the public website */}
      <header className="header">
        <div className="container header-inner">

          <Link
            to="/"
            className="brand"
            aria-label="JonoSeba home"
          >
            <span className="brand-icon">
              <Landmark size={25} />
            </span>

            <span className="brand-words">
              <strong>জনসেবা</strong>
              <small>JONOSEBA</small>
            </span>
          </Link>

          <nav
            className={
              `navigation ${menuOpen ? "open" : ""}`
            }
            aria-label="Main navigation"
          >
            {navigation.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                end={item.end}
                className={({ isActive }) =>
                  isActive
                    ? "nav-link active"
                    : "nav-link"
                }
                onClick={() => setMenuOpen(false)}
              >
                {item.label}
              </NavLink>
            ))}

            <Link
              to={user ? "/dashboard" : "/login"}
              className="mobile-login"
              onClick={() => setMenuOpen(false)}
            >
              {user
                ? english
                  ? "Dashboard"
                  : "ড্যাশবোর্ড"
                : english
                  ? "Sign In"
                  : "লগইন"}
            </Link>
          </nav>

          <div className="header-controls">

            {/* Bengali / English language switch */}
            <div
              className="language-control"
              role="group"
              aria-label={
                english ? "Language" : "ভাষা"
              }
            >
              <Languages size={16} />

              <button
                type="button"
                className={
                  language === "bn" ? "selected" : ""
                }
                aria-pressed={language === "bn"}
                onClick={() =>
                  void changeAppLanguage("bn")
                }
              >
                বাংলা
              </button>

              <span className="language-separator">
                /
              </span>

              <button
                type="button"
                className={
                  language === "en" ? "selected" : ""
                }
                aria-pressed={language === "en"}
                onClick={() =>
                  void changeAppLanguage("en")
                }
              >
                EN
              </button>
            </div>

            {/* Dark / Light theme */}
            <button
              type="button"
              className="theme-toggle"
              aria-label={
                english
                  ? "Change theme"
                  : "থিম পরিবর্তন করুন"
              }
              title={
                theme === "light"
                  ? "Dark mode"
                  : "Light mode"
              }
              onClick={() =>
                setTheme((current) =>
                  current === "light"
                    ? "dark"
                    : "light"
                )
              }
            >
              {theme === "light" ? (
                <Moon size={19} />
              ) : (
                <Sun size={19} />
              )}
            </button>

            {/* Account navigation */}
            <Link
              to={user ? "/dashboard" : "/login"}
              className="header-login"
            >
              {user
                ? english
                  ? "Dashboard"
                  : "ড্যাশবোর্ড"
                : english
                  ? "Sign In"
                  : "লগইন"}

              <ArrowUpRight size={16} />
            </Link>

            {/* Mobile menu */}
            <button
              type="button"
              className="menu-toggle"
              aria-label={
                menuOpen
                  ? english
                    ? "Close menu"
                    : "মেনু বন্ধ করুন"
                  : english
                    ? "Open menu"
                    : "মেনু খুলুন"
              }
              aria-expanded={menuOpen}
              onClick={() =>
                setMenuOpen((current) => !current)
              }
            >
              {menuOpen ? (
                <X size={22} />
              ) : (
                <Menu size={22} />
              )}
            </button>
          </div>
        </div>
      </header>

      <main className="auth-screen-main">
        {children}
      </main>

      <footer className="auth-screen-footer">
        {english
          ? "JonoSeba · Educational demo · Not an official government portal"
          : "জনসেবা · শিক্ষামূলক ডেমো · সরকারি অনুমোদিত পোর্টাল নয়"}
      </footer>
    </div>
  );
}


export function LoginPage() {
  const english = useEnglish();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const { user, loading, signIn } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [showPassword, setShowPassword] =
    useState(false);

  const [submitting, setSubmitting] =
    useState(false);

  const [error, setError] = useState("");

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setError("");
    setSubmitting(true);

    try {
      await signIn({
        email: email.trim().toLowerCase(),
        password,
      });

      navigate("/dashboard", {
        replace: true,
      });
    } catch (caught) {
      setError(
        caught instanceof Error
          ? caught.message
          : "Login failed. Please try again.",
      );
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) {
    return (
      <AuthLayout>
        <p className="auth-loading">
          {english
            ? "Loading..."
            : "লোড হচ্ছে..."}
        </p>
      </AuthLayout>
    );
  }

  if (user) {
    return (
      <Navigate to="/dashboard" replace />
    );
  }

  return (
    <AuthLayout>
      <div className="auth-form-card">

        <div className="auth-form-heading">
          <span className="auth-heading-icon">
            <LockKeyhole size={26} />
          </span>

          <h1>
            {english
              ? "Welcome back"
              : "আবারও স্বাগতম"}
          </h1>

          <p>
            {english
              ? "Sign in to your JonoSeba account."
              : "আপনার জনসেবা অ্যাকাউন্টে লগইন করুন।"}
          </p>
        </div>

        {searchParams.get("registered") === "1" && (
          <p
            className="auth-success"
            role="status"
          >
            {english
              ? "Registration successful. You can now sign in."
              : "নিবন্ধন সফল হয়েছে। এখন লগইন করুন।"}
          </p>
        )}

        {error && (
          <p
            className="auth-error"
            role="alert"
          >
            {error}
          </p>
        )}

        <form
          className="auth-form"
          onSubmit={(event) =>
            void handleSubmit(event)
          }
        >

          <label htmlFor="login-email">
            {english
              ? "Email address"
              : "ইমেইল"}
          </label>

          <div className="auth-input-wrap">
            <Mail size={18} aria-hidden="true" />

            <input
              id="login-email"
              type="email"
              autoComplete="email"
              placeholder="name@example.com"
              value={email}
              onChange={(event) =>
                setEmail(event.target.value)
              }
              required
            />
          </div>

          <label htmlFor="login-password">
            {english
              ? "Password"
              : "পাসওয়ার্ড"}
          </label>

          <div className="auth-input-wrap">
            <LockKeyhole
              size={18}
              aria-hidden="true"
            />

            <input
              id="login-password"
              type={
                showPassword
                  ? "text"
                  : "password"
              }
              autoComplete="current-password"
              placeholder="••••••••"
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
              required
            />

            <button
              type="button"
              className="auth-password-toggle"
              onClick={() =>
                setShowPassword((value) => !value)
              }
              aria-label={
                showPassword
                  ? "Hide password"
                  : "Show password"
              }
            >
              {showPassword ? (
                <EyeOff size={18} />
              ) : (
                <Eye size={18} />
              )}
            </button>
          </div>

          <button
            type="submit"
            className="auth-submit"
            disabled={submitting}
          >
            {submitting
              ? english
                ? "Signing in..."
                : "লগইন হচ্ছে..."
              : english
                ? "Sign In"
                : "লগইন"}

            <ArrowRight size={18} />
          </button>
        </form>

        <p className="auth-switch-link">
          {english
            ? "Don't have an account?"
            : "অ্যাকাউন্ট নেই?"}{" "}

          <Link to="/register">
            {english
              ? "Register"
              : "নিবন্ধন করুন"}
          </Link>
        </p>

        <Link
          to="/"
          className="auth-back-link"
        >
          <ArrowLeft size={17} />

          {english
            ? "Back to home"
            : "হোমে ফিরে যান"}
        </Link>
      </div>
    </AuthLayout>
  );
}


export function RegisterPage() {
  const english = useEnglish();
  const navigate = useNavigate();

  const { user, loading } = useAuth();

  const [fullName, setFullName] =
    useState("");

  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [confirmPassword, setConfirmPassword] =
    useState("");

  const [showPassword, setShowPassword] =
    useState(false);

  const [submitting, setSubmitting] =
    useState(false);

  const [error, setError] =
    useState("");

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();
    setError("");

    if (fullName.trim().length < 2) {
      setError(
        english
          ? "Full name must contain at least 2 characters."
          : "নাম কমপক্ষে ২ অক্ষরের হতে হবে।",
      );
      return;
    }

    if (
      password.length < 8 ||
      password.length > 128
    ) {
      setError(
        english
          ? "Password must contain 8–128 characters."
          : "পাসওয়ার্ড ৮–১২৮ অক্ষরের হতে হবে।",
      );
      return;
    }

    if (password !== confirmPassword) {
      setError(
        english
          ? "Passwords do not match."
          : "দুইটি পাসওয়ার্ড এক নয়।",
      );
      return;
    }

    setSubmitting(true);

    try {
      await registerCitizen({
        full_name: fullName.trim(),
        email: email.trim().toLowerCase(),
        password,
      });

      navigate("/login?registered=1", {
        replace: true,
      });
    } catch (caught) {
      setError(
        caught instanceof ApiError ||
        caught instanceof Error
          ? caught.message
          : "Registration failed. Please try again.",
      );
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) {
    return (
      <AuthLayout>
        <p className="auth-loading">
          {english
            ? "Loading..."
            : "লোড হচ্ছে..."}
        </p>
      </AuthLayout>
    );
  }

  if (user) {
    return (
      <Navigate to="/dashboard" replace />
    );
  }

  return (
    <AuthLayout>
      <div className="auth-form-card">

        <div className="auth-form-heading">
          <span className="auth-heading-icon">
            <UserRound size={26} />
          </span>

          <h1>
            {english
              ? "Create your account"
              : "নতুন অ্যাকাউন্ট তৈরি করুন"}
          </h1>

          <p>
            {english
              ? "Register as a JonoSeba citizen user."
              : "জনসেবায় নাগরিক হিসেবে নিবন্ধন করুন।"}
          </p>
        </div>

        {error && (
          <p
            className="auth-error"
            role="alert"
          >
            {error}
          </p>
        )}

        <form
          className="auth-form"
          onSubmit={(event) =>
            void handleSubmit(event)
          }
        >

          <label htmlFor="register-name">
            {english
              ? "Full name"
              : "পুরো নাম"}
          </label>

          <div className="auth-input-wrap">
            <UserRound
              size={18}
              aria-hidden="true"
            />

            <input
              id="register-name"
              type="text"
              autoComplete="name"
              minLength={2}
              maxLength={150}
              placeholder={
                english
                  ? "Your full name"
                  : "আপনার পুরো নাম"
              }
              value={fullName}
              onChange={(event) =>
                setFullName(event.target.value)
              }
              required
            />
          </div>

          <label htmlFor="register-email">
            {english
              ? "Email address"
              : "ইমেইল"}
          </label>

          <div className="auth-input-wrap">
            <Mail
              size={18}
              aria-hidden="true"
            />

            <input
              id="register-email"
              type="email"
              autoComplete="email"
              placeholder="name@example.com"
              value={email}
              onChange={(event) =>
                setEmail(event.target.value)
              }
              required
            />
          </div>

          <label htmlFor="register-password">
            {english
              ? "Password"
              : "পাসওয়ার্ড"}
          </label>

          <div className="auth-input-wrap">
            <LockKeyhole
              size={18}
              aria-hidden="true"
            />

            <input
              id="register-password"
              type={
                showPassword
                  ? "text"
                  : "password"
              }
              autoComplete="new-password"
              minLength={8}
              maxLength={128}
              placeholder="••••••••"
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
              required
            />

            <button
              type="button"
              className="auth-password-toggle"
              onClick={() =>
                setShowPassword((value) => !value)
              }
              aria-label={
                showPassword
                  ? "Hide password"
                  : "Show password"
              }
            >
              {showPassword ? (
                <EyeOff size={18} />
              ) : (
                <Eye size={18} />
              )}
            </button>
          </div>

          <label htmlFor="register-confirm">
            {english
              ? "Confirm password"
              : "পাসওয়ার্ড নিশ্চিত করুন"}
          </label>

          <div className="auth-input-wrap">
            <ShieldCheck
              size={18}
              aria-hidden="true"
            />

            <input
              id="register-confirm"
              type={
                showPassword
                  ? "text"
                  : "password"
              }
              autoComplete="new-password"
              minLength={8}
              maxLength={128}
              placeholder="••••••••"
              value={confirmPassword}
              onChange={(event) =>
                setConfirmPassword(
                  event.target.value
                )
              }
              required
            />
          </div>

          <button
            type="submit"
            className="auth-submit"
            disabled={submitting}
          >
            {submitting
              ? english
                ? "Creating account..."
                : "অ্যাকাউন্ট তৈরি হচ্ছে..."
              : english
                ? "Create Account"
                : "নিবন্ধন করুন"}

            <ArrowRight size={18} />
          </button>
        </form>

        <p className="auth-switch-link">
          {english
            ? "Already have an account?"
            : "আগেই অ্যাকাউন্ট আছে?"}{" "}

          <Link to="/login">
            {english
              ? "Sign In"
              : "লগইন করুন"}
          </Link>
        </p>

        <Link
          to="/"
          className="auth-back-link"
        >
          <ArrowLeft size={17} />

          {english
            ? "Back to home"
            : "হোমে ফিরে যান"}
        </Link>
      </div>
    </AuthLayout>
  );
}


export function CitizenDashboardPage() {
  const english = useEnglish();
  const navigate = useNavigate();

  const {
    user,
    loading,
    signOut,
  } = useAuth();

  if (loading) {
    return (
      <AuthLayout>
        <p className="auth-loading">
          {english
            ? "Loading profile..."
            : "প্রোফাইল লোড হচ্ছে..."}
        </p>
      </AuthLayout>
    );
  }

  if (!user) {
    return (
      <Navigate to="/login" replace />
    );
  }

  function logout() {
    signOut();

    navigate("/login", {
      replace: true,
    });
  }

  return (
    <AuthLayout>
      <div className="citizen-dashboard">

        <div className="dashboard-welcome">
          <span className="auth-heading-icon">
            <UserRound size={26} />
          </span>

          <div>
            <h1>
              {english
                ? "Welcome,"
                : "স্বাগতম,"}{" "}
              {user.full_name}
            </h1>

            <p>
              {english
                ? "Your account is connected to the FastAPI backend."
                : "আপনার অ্যাকাউন্ট FastAPI backend-এর সঙ্গে যুক্ত হয়েছে।"}
            </p>
          </div>
        </div>

        <div className="dashboard-profile-card">
          <h2>
            {english
              ? "Your profile"
              : "আপনার প্রোফাইল"}
          </h2>

          <dl>
            <div>
              <dt>
                {english ? "Name" : "নাম"}
              </dt>
              <dd>{user.full_name}</dd>
            </div>

            <div>
              <dt>
                {english ? "Email" : "ইমেইল"}
              </dt>
              <dd>{user.email}</dd>
            </div>

            <div>
              <dt>
                {english ? "Role" : "ভূমিকা"}
              </dt>
              <dd>{user.role}</dd>
            </div>

            <div>
              <dt>
                {english
                  ? "Account status"
                  : "অ্যাকাউন্টের অবস্থা"}
              </dt>

              <dd>
                {user.is_active
                  ? english
                    ? "Active"
                    : "সক্রিয়"
                  : english
                    ? "Inactive"
                    : "নিষ্ক্রিয়"}
              </dd>
            </div>
          </dl>
        </div>

        <div className="dashboard-next-card">
          <ShieldCheck size={22} />

          <p>
            {english
              ? "Complaint submission, tracking, and your floating AI assistant will be added in the next stages."
              : "পরবর্তী ধাপে অভিযোগ জমা, ট্র্যাকিং এবং floating AI assistant যুক্ত হবে।"}
          </p>
        </div>

        <div className="dashboard-actions">
          <Link
            to="/"
            className="auth-back-link"
          >
            <ArrowLeft size={17} />
            {english ? "Home" : "হোম"}
          </Link>

          <button
            type="button"
            className="dashboard-logout"
            onClick={logout}
          >
            <LogOut size={18} />

            {english
              ? "Log Out"
              : "লগআউট"}
          </button>
        </div>
      </div>
    </AuthLayout>
  );
}
