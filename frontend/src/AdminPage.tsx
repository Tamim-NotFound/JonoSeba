import { useEffect, useMemo, useState } from "react";
import {
  Link,
  Navigate,
  NavLink,
  useNavigate,
} from "react-router-dom";
import { useTranslation } from "react-i18next";

import {
  ArrowRight,
  CheckCircle2,
  ClipboardList,
  Clock3,
  Landmark,
  Languages,
  LayoutDashboard,
  LogOut,
  Menu,
  Moon,
  RefreshCw,
  Search,
  ShieldCheck,
  Sun,
  X,
} from "lucide-react";

import { useAuth } from "./AuthContext";
import { changeAppLanguage } from "./i18n";
import { apiGet, apiPatch } from "./api/client";

import type {
  Complaint,
  ComplaintStatus,
} from "./api/complaints";

import "./admin.css";

type Theme = "light" | "dark";
type Language = "bn" | "en";

const STATUSES: ComplaintStatus[] = [
  "pending",
  "in_progress",
  "resolved",
  "rejected",
];

const TEXT = {
  en: {
    home: "Home",
    services: "Services",
    how: "How it works",
    ai: "AI Assistant",
    about: "About",
    dashboard: "Dashboard",
    administrator: "Administrator",
    logout: "Logout",
    menu: "Open navigation menu",
    theme: "Toggle light or dark mode",
    publicSite: "Public website",
    eyebrow: "JONOSEBA · ADMIN WORKSPACE",
    welcome: "Welcome back",
    heroText:
      "Review citizen complaints, manage their progress and help your city move forward.",

    total: "Total complaints",
    pending: "Pending",
    progress: "In progress",
    resolved: "Resolved",

    management: "Complaint management",
    managementDesc:
      "Review every citizen complaint and save updates directly to the database.",

    refresh: "Refresh",
    search: "Search by ID, title or location",
    allStatuses: "All statuses",
    loading: "Loading complaints...",
    loadError: "Complaint data could not be loaded.",
    empty: "No matching complaints found.",

    updateStatus: "Update status",
    saveStatus: "Save status",
    saving: "Saving...",

    location: "Location",
    department: "Department",
    citizen: "Citizen",
    submitted: "Submitted",
    updated: "Updated",
    changed: "Complaint status updated successfully",

    accessTitle: "Admin access required",
    accessDesc:
      "Only authorized administrators can access this dashboard.",
    backCitizen: "Back to citizen dashboard",
    checking: "Checking your account...",

    footerDesc:
      "A citizen-service project built for clearer complaints and better communication.",
    footerTitle: "JonoSeba",

    statuses: {
      pending: "Pending",
      in_progress: "In progress",
      resolved: "Resolved",
      rejected: "Rejected",
    },
  },

  bn: {
    home: "হোম",
    services: "সেবাসমূহ",
    how: "যেভাবে কাজ করে",
    ai: "AI সহকারী",
    about: "সম্পর্কে",
    dashboard: "ড্যাশবোর্ড",
    administrator: "অ্যাডমিন",
    logout: "লগআউট",
    menu: "নেভিগেশন মেনু খুলুন",
    theme: "ডার্ক বা লাইট মোড পরিবর্তন করুন",
    publicSite: "পাবলিক ওয়েবসাইট",
    eyebrow: "জনসেবা · অ্যাডমিন ওয়ার্কস্পেস",
    welcome: "স্বাগতম",
    heroText:
      "নাগরিকদের অভিযোগ দেখুন, অগ্রগতি পরিচালনা করুন এবং আপনার শহরের সেবাকে এগিয়ে নিন।",

    total: "মোট অভিযোগ",
    pending: "অপেক্ষমাণ",
    progress: "চলমান",
    resolved: "সমাধান হয়েছে",

    management: "অভিযোগ ব্যবস্থাপনা",
    managementDesc:
      "সকল নাগরিকের অভিযোগ পর্যালোচনা করুন এবং সরাসরি ডেটাবেজে স্ট্যাটাস সংরক্ষণ করুন।",

    refresh: "রিফ্রেশ",
    search: "ID, শিরোনাম বা স্থান দিয়ে খুঁজুন",
    allStatuses: "সব স্ট্যাটাস",
    loading: "অভিযোগ লোড হচ্ছে...",
    loadError: "অভিযোগের তথ্য লোড করা যায়নি।",
    empty: "মিল পাওয়া কোনো অভিযোগ নেই।",

    updateStatus: "স্ট্যাটাস পরিবর্তন",
    saveStatus: "স্ট্যাটাস সংরক্ষণ",
    saving: "সংরক্ষণ হচ্ছে...",

    location: "স্থান",
    department: "বিভাগ",
    citizen: "নাগরিক",
    submitted: "জমা হয়েছে",
    updated: "সর্বশেষ আপডেট",
    changed: "অভিযোগের স্ট্যাটাস সফলভাবে আপডেট হয়েছে",

    accessTitle: "অ্যাডমিন অনুমতি প্রয়োজন",
    accessDesc:
      "শুধু অনুমোদিত অ্যাডমিন এই ড্যাশবোর্ড ব্যবহার করতে পারবেন।",
    backCitizen: "নাগরিক ড্যাশবোর্ডে ফিরুন",
    checking: "অ্যাকাউন্ট যাচাই করা হচ্ছে...",

    footerDesc:
      "নাগরিক অভিযোগ ও যোগাযোগ সহজ করার লক্ষ্যে তৈরি একটি জনসেবা প্রকল্প।",
    footerTitle: "জনসেবা",

    statuses: {
      pending: "অপেক্ষমাণ",
      in_progress: "চলমান",
      resolved: "সমাধান হয়েছে",
      rejected: "বাতিল",
    },
  },
} as const;

const NAV_ITEMS = [
  {
    to: "/admin",
    key: "dashboard",
  },
] as const;

function readTheme(): Theme {
  try {
    const saved =
      localStorage.getItem("jonoseba-theme") ??
      localStorage.getItem("jonoseba-admin-theme");

    return saved === "light" || saved === "dark"
      ? saved
      : "dark";
  } catch {
    return "dark";
  }
}

function formatDate(
  value: string,
  language: Language,
): string {
  const date = new Date(value);

  return Number.isNaN(date.getTime())
    ? value
    : date.toLocaleString(
        language === "bn" ? "bn-BD" : "en-GB",
      );
}

function errorMessage(error: unknown): string {
  return error instanceof Error
    ? error.message
    : "Something went wrong.";
}

/*
  Bangladesh skyline.

  Building, flag and slogan are kept
  consistent with the Citizen Dashboard.
*/
function BangladeshSkyline() {
  return (
    <svg
      className="ja-skyline"
      viewBox="0 0 680 190"
      aria-hidden="true"
      focusable="false"
    >
      <path
        d="M0 178Q140 130 280 161T680 153V190H0Z"
        fill="#73d9c8"
        opacity=".36"
      />

      <g fill="#42b4ab" opacity=".36">
        <rect x="65" y="83" width="53" height="95" rx="3" />
        <rect x="131" y="58" width="41" height="120" rx="3" />
        <rect x="190" y="99" width="63" height="79" rx="3" />
        <rect x="476" y="76" width="56" height="102" rx="3" />
        <rect x="543" y="54" width="48" height="124" rx="3" />
        <rect x="605" y="92" width="47" height="86" rx="3" />
      </g>

      <g fill="#eafcf7" opacity=".7">
        {[
          84, 104, 147, 210, 229,
          492, 513, 558, 577, 622, 639,
        ].map((x) => (
          <rect
            key={x}
            x={x}
            y="117"
            width="8"
            height="13"
            rx="2"
          />
        ))}
      </g>

      <rect
        x="291"
        y="80"
        width="178"
        height="96"
        rx="5"
        fill="#ecfffb"
      />

      <path
        d="M275 79L380 27L485 79Z"
        fill="#0a9789"
      />

      <rect
        x="277"
        y="79"
        width="207"
        height="12"
        rx="3"
        fill="#087a76"
      />

      <rect
        x="364"
        y="110"
        width="33"
        height="66"
        rx="16"
        fill="#0d8079"
      />

      {[312, 341, 411, 440].map((x) => (
        <rect
          key={x}
          x={x}
          y="105"
          width="17"
          height="54"
          rx="3"
          fill="#8cd5c9"
        />
      ))}

      <path
        d="M280 177H481"
        stroke="#049a88"
        strokeWidth="8"
        strokeLinecap="round"
      />

      <path
        d="M379 27V8"
        stroke="#087a76"
        strokeWidth="3"
      />

      <rect
        x="380"
        y="8"
        width="25"
        height="15"
        fill="#006A4E"
      />

      <circle
        cx="389.5"
        cy="15.5"
        r="5"
        fill="#F42A41"
      />

      <text
        x="380"
        y="103"
        fontSize="12"
        textAnchor="middle"
        textLength="170"
        lengthAdjust="spacingAndGlyphs"
        fill="#07675f"
        fontWeight="bold"
      >
        {"আপনার "}
        <tspan fill="#DC2626">শহর</tspan>
        {", আপনার "}
        <tspan fill="#DC2626">সেবা</tspan>
        {", আপনার "}
        <tspan fill="#DC2626">হাতেই</tspan>
      </text>

      <g fill="#27a98b">
        <circle cx="259" cy="132" r="28" />
        <circle cx="234" cy="144" r="21" />
        <circle cx="506" cy="134" r="29" />
        <circle cx="531" cy="146" r="22" />
      </g>
    </svg>
  );
}

export default function AdminPage() {
  const {
    user,
    loading: authLoading,
    signOut,
  } = useAuth();

  const navigate = useNavigate();
  const { i18n } = useTranslation();

  const language: Language =
    i18n.resolvedLanguage === "en"
      ? "en"
      : "bn";

  const copy = TEXT[language];

  const [theme, setTheme] =
    useState<Theme>(readTheme);

  const [menuOpen, setMenuOpen] =
    useState(false);

  const [complaints, setComplaints] =
    useState<Complaint[]>([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState("all");

  const [busyId, setBusyId] =
    useState<number | null>(null);

  const [
    selectedStatuses,
    setSelectedStatuses,
  ] = useState<Record<number, ComplaintStatus>>({});

  const [revision, setRevision] =
    useState(0);

  const isAdmin = user?.role === "admin";

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
    if (!isAdmin) {
      return;
    }

    let active = true;

    setLoading(true);
    setError("");

    void apiGet<Complaint[]>("/complaints")
      .then((result) => {
        if (!active) {
          return;
        }

        if (!Array.isArray(result)) {
          throw new Error(
            "Unexpected complaints API response.",
          );
        }

        setComplaints(result);

        const next: Record<
          number,
          ComplaintStatus
        > = {};

        result.forEach((item) => {
          next[item.id] = item.status;
        });

        setSelectedStatuses(next);
      })
      .catch((reason: unknown) => {
        if (active) {
          setError(errorMessage(reason));
        }
      })
      .finally(() => {
        if (active) {
          setLoading(false);
        }
      });

    return () => {
      active = false;
    };
  }, [isAdmin, revision]);

  const filtered = useMemo(() => {
    const query = search.trim().toLowerCase();

    return complaints
      .filter(
        (item) =>
          (filter === "all" ||
            item.status === filter) &&
          (!query ||
            String(item.id).includes(query) ||
            item.title.toLowerCase().includes(query) ||
            item.location.toLowerCase().includes(query)),
      )
      .sort((a, b) =>
        b.created_at.localeCompare(a.created_at),
      );
  }, [complaints, filter, search]);

  const counts = useMemo(
    () => ({
      total: complaints.length,
      pending: complaints.filter(
        (c) => c.status === "pending",
      ).length,
      progress: complaints.filter(
        (c) => c.status === "in_progress",
      ).length,
      resolved: complaints.filter(
        (c) => c.status === "resolved",
      ).length,
    }),
    [complaints],
  );

  async function updateStatus(item: Complaint) {
    const status = selectedStatuses[item.id];

    if (
      !status ||
      status === item.status ||
      busyId !== null
    ) {
      return;
    }

    setBusyId(item.id);
    setError("");
    setNotice("");

    try {
      const updated = await apiPatch<Complaint>(
        `/complaints/${item.id}`,
        { status },
      );

      if (updated.id !== item.id) {
        throw new Error(
          "Unexpected complaint response from API.",
        );
      }

      setComplaints((current) =>
        current.map((c) =>
          c.id === updated.id ? updated : c,
        ),
      );

      setSelectedStatuses((current) => ({
        ...current,
        [updated.id]: updated.status,
      }));

      setNotice(
        `${copy.changed}: #${updated.id} — ${
          copy.statuses[updated.status]
        }`,
      );
    } catch (reason) {
      setError(errorMessage(reason));

      setSelectedStatuses((current) => ({
        ...current,
        [item.id]: item.status,
      }));
    } finally {
      setBusyId(null);
    }
  }

  function logout() {
    signOut();
    navigate("/login", { replace: true });
  }

  if (authLoading) {
    return (
      <div className="ja-access" role="status">
        {copy.checking}
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (!isAdmin) {
    return (
      <div className="ja-access">
        <ShieldCheck size={40} />

        <h1>{copy.accessTitle}</h1>
        <p>{copy.accessDesc}</p>

        <Link
          className="ja-btn ja-btn-primary"
          to="/dashboard"
        >
          {copy.backCitizen}
        </Link>
      </div>
    );
  }

  return (
    <div className={`ja-page ja-theme-${theme}`}>
      <header className="ja-header">
        <div className="ja-header-inner">
          <Link
            className="ja-brand"
            to="/admin"
            onClick={() => setMenuOpen(false)}
          >
            {/* Same building logo as Citizen Dashboard */}
            <span className="ja-brand-icon">
              <Landmark size={24} />
            </span>

            <span className="ja-brand-name">
              <strong>জনসেবা</strong>
              <small>JONOSEBA ADMIN</small>
            </span>
          </Link>

          <nav
            className={`ja-nav ${
              menuOpen ? "ja-nav-open" : ""
            }`}
            aria-label="Admin navigation"
          >
            {NAV_ITEMS.map(({ to, key }) => (
              <NavLink
                key={key}
                to={to}
                end
                  
                
                onClick={() => setMenuOpen(false)}
                className={({ isActive }) =>
                  `ja-nav-link${
                    isActive ? " ja-nav-active" : ""
                  }`
                }
              >
                {copy[key]}
              </NavLink>
            ))}
          </nav>

          <div className="ja-header-actions">
            <div
              className="ja-language"
              role="group"
              aria-label="Language"
            >
              <Languages size={15} />

              <button
                type="button"
                className={
                  language === "bn"
                    ? "ja-selected"
                    : ""
                }
                aria-pressed={language === "bn"}
                onClick={() =>
                  void changeAppLanguage("bn")
                }
              >
                বাংলা
              </button>

              <span>/</span>

              <button
                type="button"
                className={
                  language === "en"
                    ? "ja-selected"
                    : ""
                }
                aria-pressed={language === "en"}
                onClick={() =>
                  void changeAppLanguage("en")
                }
              >
                EN
              </button>
            </div>

            <button
              className="ja-icon-button"
              type="button"
              title={copy.theme}
              aria-label={copy.theme}
              onClick={() =>
                setTheme((value) =>
                  value === "dark"
                    ? "light"
                    : "dark",
                )
              }
            >
              {theme === "dark" ? (
                <Sun size={19} />
              ) : (
                <Moon size={19} />
              )}
            </button>

            <div
              className="ja-account"
              title={user.email}
            >
              <span className="ja-avatar">
                {user.full_name
                  .trim()
                  .charAt(0)
                  .toUpperCase()}
              </span>

              <span className="ja-account-copy">
                <strong>{user.full_name}</strong>
                <small>{copy.administrator}</small>
              </span>
            </div>

            <button
              type="button"
              className="ja-logout"
              onClick={logout}
            >
              <LogOut size={16} />
              <span>{copy.logout}</span>
            </button>

            <button
              className="ja-menu-button"
              type="button"
              aria-label={copy.menu}
              aria-expanded={menuOpen}
              onClick={() =>
                setMenuOpen((value) => !value)
              }
            >
              {menuOpen ? (
                <X size={21} />
              ) : (
                <Menu size={21} />
              )}
            </button>
          </div>
        </div>
      </header>

      <main className="ja-main">
        <section className="ja-hero">
          <div className="ja-hero-content">
            <div className="ja-hero-eyebrow">
              <span className="ja-hero-line" />
              {copy.eyebrow}
            </div>

            <h1>
              {copy.welcome},{" "}
              <span>{user.full_name}!</span>
            </h1>

            <p>{copy.heroText}</p>

            <Link
              to="/"
              className="ja-hero-link"
            >
              {copy.publicSite}
              <ArrowRight size={15} />
            </Link>
          </div>

          <div className="ja-hero-art">
            <BangladeshSkyline />
          </div>
        </section>

        <section
          className="ja-stats"
          aria-label="Complaint statistics"
        >
          {([
            {
              title: copy.total,
              value: counts.total,
              Icon: ClipboardList,
              tone: "teal",
            },
            {
              title: copy.pending,
              value: counts.pending,
              Icon: Clock3,
              tone: "amber",
            },
            {
              title: copy.progress,
              value: counts.progress,
              Icon: RefreshCw,
              tone: "blue",
            },
            {
              title: copy.resolved,
              value: counts.resolved,
              Icon: CheckCircle2,
              tone: "green",
            },
          ] as const).map(
            ({ title, value, Icon, tone }) => (
              <div
                className={`ja-stat ja-stat-${tone}`}
                key={tone}
              >
                <span className="ja-stat-icon">
                  <Icon size={21} />
                </span>

                <div>
                  <span className="ja-stat-label">
                    {title}
                  </span>

                  <strong>
                    {loading || error
                      ? "—"
                      : value}
                  </strong>
                </div>
              </div>
            ),
          )}
        </section>

        {notice && (
          <div
            className="ja-notice ja-notice-success"
            role="status"
          >
            <CheckCircle2 size={18} />
            {notice}
          </div>
        )}

        {error && (
          <div
            className="ja-notice ja-notice-error"
            role="alert"
          >
            {error}
          </div>
        )}

        <section className="ja-panel">
          <div className="ja-panel-heading">
            <div className="ja-panel-title">
              <span className="ja-panel-symbol">
                <LayoutDashboard size={20} />
              </span>

              <div>
                <h2>{copy.management}</h2>
                <p>{copy.managementDesc}</p>
              </div>
            </div>

            <button
              className="ja-btn ja-btn-quiet"
              type="button"
              disabled={
                loading ||
                busyId !== null
              }
              onClick={() => {
                setNotice("");
                setRevision((n) => n + 1);
              }}
            >
              <RefreshCw size={17} />
              {copy.refresh}
            </button>
          </div>

          <div className="ja-toolbar">
            <label className="ja-search">
              <Search size={18} />

              <input
                type="search"
                value={search}
                placeholder={copy.search}
                onChange={(event) =>
                  setSearch(event.target.value)
                }
                aria-label={copy.search}
              />
            </label>

            <select
              className="ja-filter"
              value={filter}
              aria-label={copy.allStatuses}
              onChange={(event) =>
                setFilter(event.target.value)
              }
            >
              <option value="all">
                {copy.allStatuses}
              </option>

              {STATUSES.map((status) => (
                <option
                  value={status}
                  key={status}
                >
                  {copy.statuses[status]}
                </option>
              ))}
            </select>
          </div>

          {loading ? (
            <div
              className="ja-empty"
              role="status"
            >
              {copy.loading}
            </div>
          ) : error &&
            complaints.length === 0 ? (
            <div className="ja-empty">
              {copy.loadError}
            </div>
          ) : filtered.length === 0 ? (
            <div className="ja-empty">
              {copy.empty}
            </div>
          ) : (
            <div className="ja-complaint-list">
              {filtered.map((item) => (
                <article
                  className="ja-complaint"
                  key={item.id}
                >
                  <div className="ja-complaint-info">
                    <div className="ja-complaint-top">
                      <span className="ja-complaint-id">
                        #{item.id}
                      </span>

                      <span
                        className={`ja-status ja-status-${item.status}`}
                      >
                        {copy.statuses[item.status]}
                      </span>
                    </div>

                    <h3>{item.title}</h3>

                    <p className="ja-description">
                      {item.description}
                    </p>

                    <div className="ja-meta">
                      <span>
                        <strong>
                          {copy.location}:
                        </strong>{" "}
                        {item.location}
                      </span>

                      <span>
                        <strong>
                          {copy.department}:
                        </strong>{" "}
                        #{item.department_id}
                      </span>

                      <span>
                        <strong>
                          {copy.citizen}:
                        </strong>{" "}
                        #{item.citizen_id}
                      </span>

                      <span>
                        <strong>
                          {copy.submitted}:
                        </strong>{" "}
                        {formatDate(
                          item.created_at,
                          language,
                        )}
                      </span>

                      <span>
                        <strong>
                          {copy.updated}:
                        </strong>{" "}
                        {formatDate(
                          item.updated_at,
                          language,
                        )}
                      </span>
                    </div>
                  </div>

                  <div className="ja-complaint-controls">
                    <label
                      htmlFor={`ja-status-${item.id}`}
                    >
                      {copy.updateStatus}
                    </label>

                    <select
                      id={`ja-status-${item.id}`}
                      value={
                        selectedStatuses[item.id] ??
                        item.status
                      }
                      disabled={busyId !== null}
                      onChange={(event) =>
                        setSelectedStatuses(
                          (current) => ({
                            ...current,
                            [item.id]:
                              event.target
                                .value as ComplaintStatus,
                          }),
                        )
                      }
                    >
                      {STATUSES.map((status) => (
                        <option
                          key={status}
                          value={status}
                        >
                          {copy.statuses[status]}
                        </option>
                      ))}
                    </select>

                    <button
                      type="button"
                      className="ja-btn ja-btn-primary"
                      disabled={
                        busyId !== null ||
                        (selectedStatuses[item.id] ??
                          item.status) ===
                          item.status
                      }
                      onClick={() =>
                        void updateStatus(item)
                      }
                    >
                      {busyId === item.id
                        ? copy.saving
                        : copy.saveStatus}
                    </button>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>
      </main>

      <footer className="ja-footer">
        <div className="ja-footer-inner">
          <div className="ja-footer-brand">
            <span className="ja-footer-emblem">
              <Landmark size={23} />
            </span>

            <div>
              <strong>{copy.footerTitle}</strong>
              <small>
                JONOSEBA · CITIZEN SERVICES
              </small>
            </div>
          </div>

          <p>{copy.footerDesc}</p>

          <div className="ja-footer-bottom">
            <span>
              © {new Date().getFullYear()} JonoSeba
            </span>
          </div>
        </div>
      </footer>
    </div>
  );
}
