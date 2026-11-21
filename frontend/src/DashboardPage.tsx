import {
  useEffect,
  useRef,
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
  Bookmark,
  Bot,
  CheckCircle2,
  ChevronDown,
  ClipboardList,
  Droplets,
  FilePlus2,
  FileText,
  Landmark,
  Languages,
  LayoutGrid,
  LogOut,
  MapPin,
  Menu,
  MessageCircle,
  Moon,
  RefreshCw,
  Search,
  Send,
  Settings2,
  ShieldCheck,
  Sparkles,
  Sun,
  Trash2,
  UserRound,
  X,
  type LucideIcon,
} from "lucide-react";

import { changeAppLanguage } from "./i18n";
import { useAuth } from "./AuthContext";

import {
  askJonoSeba,
  type ChatHistoryMessage,
} from "./api/chat";

import {
  getActiveDepartments,
  getMyComplaints,
  getComplaintById,
  submitComplaint,
  type Complaint,
  type ComplaintStatus,
  type Department,
} from "./api/complaints";

import "./dashboard.css";
import "./workflow.css";

type Language = "bn" | "en";
type Theme = "light" | "dark";

type DashboardView =
  | "home"
  | "new"
  | "complaints"
  | "track"
  | "profile";

type ComplaintDraft = {
  title: string;
  departmentId: string;
  ward: string;
  location: string;
  description: string;
};

const emptyDraft: ComplaintDraft = {
  title: "",
  departmentId: "",
  ward: "",
  location: "",
  description: "",
};

const words = {
  en: {
    home: "Home",
    services: "Services",
    how: "How it works",
    ai: "AI Assistant",
    about: "About",
    dashboard: "Dashboard",
    profile: "Profile",
    editProfile: "Profile settings (coming soon)",
    logout: "Logout",
    menu: "Open menu",
    theme: "Change theme",
    welcome: "Welcome back",
    welcomeText:
      "Report civic issues, track progress and explore municipal services in one place.",
    demo:
      "Educational demo — not an official government portal",

    total: "Total complaints",
    progress: "In progress",
    resolved: "Resolved",
    loading: "Loading...",
    retry: "Try again",

    newComplaint: "File new complaint",
    newDesc: "Report an issue in your area",
    track: "Track complaint",
    trackDesc: "Check its current status",
    explore: "Explore services",
    exploreDesc: "Browse municipal guidance",
    ask: "Ask AI assistant",
    askDesc: "Chat with JonoSeba",

    recent: "Recent complaints",
    viewAll: "View all",
    noRecords: "No complaints submitted yet.",
    tracking: "Complaint tracking",
    trackingEmpty:
      "Select a complaint to see its current status.",

    shortcuts: "Service shortcuts",
    shortcutsDesc: "Explore common municipal topics",
    water: "Water supply",
    lighting: "Street lighting",
    waste: "Waste management",
    birth: "Birth & death registration",
    holding: "Holding tax",
    trade: "Trade license",

    chatTitle: "JonoSeba AI Assistant",
    chatPending: "FastAPI AI chat",
    chatWelcome:
      "Ask about municipal services in Bangla, English or Banglish.",
    chatInput: "Type your question...",
    chatSend: "Send message",
    chatBusy: "Thinking...",
    closeChat: "Close chat",
    openChat: "Open chat",
    chatStatus: "AI service",

    complaintPage: "My complaints",
    complaintPageDesc:
      "Your complaints stored in the database.",
    complaintNewTitle: "New complaint",
    complaintNewDesc:
      "Submit a real complaint to the JonoSeba demo database.",

    labelTitle: "Complaint title",
    labelDepartment: "Responsible department",
    labelWard: "Ward (optional)",
    labelLocation: "Specific location",
    labelDescription: "Describe the issue",
    chooseDepartment: "Select department",

    draftSaved:
      "Draft saved in this browser session. It has NOT been submitted.",
    draftClear: "Clear form",
    draftSave: "Save draft",
    submit: "Submit complaint",
    submitting: "Submitting...",
    submitted: "Complaint created successfully!",
    receipt: "Complaint ID",
    viewStatus: "Track this complaint",

    noDepartments:
      "No active departments found. An admin must add an active department before submission.",
    locationNote:
      "Ward will be included in the location field; the backend has no separate ward field.",

    profileTitle: "Your profile",
    profileDesc:
      "Information from your authenticated account.",
    name: "Full name",
    email: "Email",
    role: "Role",
    account: "Account status",
    active: "Active",
    inactive: "Inactive",
    editPending:
      "Profile editing needs a backend update endpoint; this view is read-only.",

    trackPage: "Track a complaint",
    trackPageDesc:
      "Enter the numeric ID of your own complaint.",
    searchPlaceholder: "Complaint ID (e.g. 12)",
    find: "Find complaint",
    invalidId:
      "Enter a valid positive numeric complaint ID.",
    notOwned:
      "This complaint is not available to your account.",

    backDashboard: "Back to dashboard",
    status: "Status",
    priority: "Priority",
    department: "Department",
    location: "Location",
    created: "Submitted at",
    updated: "Last updated",
    description: "Description",

    statuses: {
      pending: "Pending",
      in_progress: "In progress",
      resolved: "Resolved",
      rejected: "Rejected",
    },

    noHistory:
      "This API returns current status and last update, not a status-history timeline.",
  },

  bn: {
    home: "হোম",
    services: "সেবাসমূহ",
    how: "যেভাবে কাজ করে",
    ai: "AI সহকারী",
    about: "সম্পর্কে",
    dashboard: "ড্যাশবোর্ড",
    profile: "প্রোফাইল",
    editProfile: "প্রোফাইল সেটিংস (শিগগিরই)",
    logout: "লগআউট",
    menu: "মেনু খুলুন",
    theme: "থিম পরিবর্তন করুন",
    welcome: "স্বাগতম",
    welcomeText:
      "এলাকার সমস্যা জানান, অভিযোগের অগ্রগতি দেখুন এবং প্রয়োজনীয় পৌরসেবা সম্পর্কে জানুন।",
    demo:
      "শিক্ষামূলক ডেমো — সরকারি অনুমোদিত পোর্টাল নয়",

    total: "মোট অভিযোগ",
    progress: "চলমান",
    resolved: "সমাধান হয়েছে",
    loading: "লোড হচ্ছে...",
    retry: "আবার চেষ্টা করুন",

    newComplaint: "নতুন অভিযোগ করুন",
    newDesc: "এলাকার সমস্যা জানান",
    track: "অভিযোগ ট্র্যাক করুন",
    trackDesc: "বর্তমান অবস্থা দেখুন",
    explore: "সেবা খুঁজুন",
    exploreDesc: "পৌরসেবার তথ্য দেখুন",
    ask: "AI সহায়তা নিন",
    askDesc: "জনসেবা AI-এর সঙ্গে কথা বলুন",

    recent: "সাম্প্রতিক অভিযোগ",
    viewAll: "সব দেখুন",
    noRecords: "এখনো কোনো অভিযোগ জমা নেই।",
    tracking: "অভিযোগের অগ্রগতি",
    trackingEmpty:
      "বর্তমান অবস্থা জানতে একটি অভিযোগ নির্বাচন করুন।",

    shortcuts: "প্রয়োজনীয় সেবা",
    shortcutsDesc: "জনপ্রিয় পৌরসেবার তথ্য দেখুন",
    water: "পানি সরবরাহ",
    lighting: "সড়কবাতি",
    waste: "বর্জ্য ব্যবস্থাপনা",
    birth: "জন্ম ও মৃত্যু নিবন্ধন",
    holding: "হোল্ডিং ট্যাক্স",
    trade: "ট্রেড লাইসেন্স",

    chatTitle: "জনসেবা AI সহকারী",
    chatPending: "FastAPI AI চ্যাট",
    chatWelcome:
      "বাংলা, ইংরেজি বা বাংলিশে পৌরসেবা সম্পর্কে জিজ্ঞাসা করুন।",
    chatInput: "আপনার প্রশ্ন লিখুন...",
    chatSend: "মেসেজ পাঠান",
    chatBusy: "উত্তর তৈরি হচ্ছে...",
    closeChat: "চ্যাট বন্ধ করুন",
    openChat: "চ্যাট খুলুন",
    chatStatus: "AI সেবা",

    complaintPage: "আমার অভিযোগসমূহ",
    complaintPageDesc:
      "ডেটাবেজে সংরক্ষিত আপনার অভিযোগের তালিকা।",
    complaintNewTitle: "নতুন অভিযোগ",
    complaintNewDesc:
      "জনসেবা ডেমো ডেটাবেজে প্রকৃত অভিযোগ জমা দিন।",

    labelTitle: "অভিযোগের শিরোনাম",
    labelDepartment: "দায়িত্বপ্রাপ্ত বিভাগ",
    labelWard: "ওয়ার্ড (ঐচ্ছিক)",
    labelLocation: "সুনির্দিষ্ট স্থান",
    labelDescription: "সমস্যার বিবরণ",
    chooseDepartment: "বিভাগ নির্বাচন করুন",

    draftSaved:
      "এই ব্রাউজার সেশনে খসড়া সংরক্ষিত হয়েছে। অভিযোগ জমা হয়নি।",
    draftClear: "ফর্ম পরিষ্কার করুন",
    draftSave: "খসড়া সংরক্ষণ",
    submit: "অভিযোগ জমা দিন",
    submitting: "জমা হচ্ছে...",
    submitted: "অভিযোগ সফলভাবে জমা হয়েছে!",
    receipt: "অভিযোগ নম্বর",
    viewStatus: "অভিযোগটি ট্র্যাক করুন",

    noDepartments:
      "কোনো সক্রিয় বিভাগ নেই। অভিযোগ পাঠানোর আগে অ্যাডমিনকে বিভাগ যোগ করতে হবে।",
    locationNote:
      "Backend-এ আলাদা ওয়ার্ড নেই, তাই ওয়ার্ড নম্বর location-এর সঙ্গে সংরক্ষিত হবে।",

    profileTitle: "আপনার প্রোফাইল",
    profileDesc:
      "লগইন করা অ্যাকাউন্টের প্রকৃত তথ্য।",
    name: "পুরো নাম",
    email: "ইমেইল",
    role: "ভূমিকা",
    account: "অ্যাকাউন্টের অবস্থা",
    active: "সক্রিয়",
    inactive: "নিষ্ক্রিয়",
    editPending:
      "প্রোফাইল পরিবর্তনের backend endpoint এখনো নেই/যাচাই হয়নি; এই পেজ read-only।",

    trackPage: "অভিযোগ ট্র্যাক করুন",
    trackPageDesc:
      "নিজের অভিযোগের সংখ্যাসূচক ID লিখুন।",
    searchPlaceholder: "অভিযোগের ID (যেমন 12)",
    find: "খুঁজুন",
    invalidId:
      "সঠিক সংখ্যাসূচক অভিযোগ ID লিখুন।",
    notOwned:
      "এই অভিযোগটি আপনার অ্যাকাউন্টে পাওয়া যায়নি।",

    backDashboard: "ড্যাশবোর্ডে ফিরুন",
    status: "অবস্থা",
    priority: "অগ্রাধিকার",
    department: "বিভাগ",
    location: "স্থান",
    created: "জমার সময়",
    updated: "সর্বশেষ পরিবর্তন",
    description: "বিবরণ",

    statuses: {
      pending: "অপেক্ষমাণ",
      in_progress: "চলমান",
      resolved: "সমাধান হয়েছে",
      rejected: "বাতিল",
    },

    noHistory:
      "এই API শুধু বর্তমান অবস্থা ও সর্বশেষ পরিবর্তন দেয়; পূর্ণ ইতিহাস দেয় না।",
  },
} as const;

function useLanguage() {
  const { i18n } = useTranslation();

  const lang: Language =
    i18n.resolvedLanguage === "en"
      ? "en"
      : "bn";

  return {
    lang,
    copy: words[lang],
  };
}

function savedTheme(): Theme {
  try {
    return localStorage.getItem("jonoseba-theme") === "dark"
      ? "dark"
      : "light";
  } catch {
    return "light";
  }
}

function friendlyError(error: unknown): string {
  return error instanceof Error
    ? error.message
    : "An unexpected error occurred.";
}

function readableDate(
  raw: string,
  lang: Language,
): string {
  const date = new Date(raw);

  return Number.isNaN(date.getTime())
    ? raw
    : date.toLocaleString(
        lang === "bn" ? "bn-BD" : "en-GB",
      );
}

function useComplaintRecords(
  userId: number | undefined,
) {
  const [items, setItems] = useState<Complaint[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [revision, setRevision] = useState(0);

  useEffect(() => {
    let active = true;

    if (!userId) {
      return;
    }

    getMyComplaints()
      .then((result) => {
        if (!active) {
          return;
        }

        if (!Array.isArray(result)) {
          throw new Error(
            "Unexpected complaint list response.",
          );
        }

        // The backend must also enforce citizen ownership.
        setItems(
          result
            .filter(
              (item) => item.citizen_id === userId,
            )
            .sort((a, b) =>
              b.created_at.localeCompare(a.created_at),
            ),
        );

        setError("");
      })
      .catch((reason: unknown) => {
        if (active) {
          setError(friendlyError(reason));
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
  }, [userId, revision]);

  return {
    items,
    loading,
    error,
    refresh: () => {
      setLoading(true);
      setRevision((n) => n + 1);
    },
  };
}

const quickServices: {
  key:
    | "water"
    | "lighting"
    | "waste"
    | "birth"
    | "holding"
    | "trade";
  route: string;
  Icon: LucideIcon;
}[] = [
  {
    key: "water",
    route: "/services/water",
    Icon: Droplets,
  },
  {
    key: "lighting",
    route: "/services",
    Icon: Sparkles,
  },
  {
    key: "waste",
    route: "/services",
    Icon: Trash2,
  },
  {
    key: "birth",
    route: "/services/birth",
    Icon: FileText,
  },
  {
    key: "holding",
    route: "/services/tax",
    Icon: Landmark,
  },
  {
    key: "trade",
    route: "/services/trade",
    Icon: ClipboardList,
  },
];

function DashboardSkyline() {
  return (
    <svg
      className="jd-skyline"
      viewBox="0 0 680 190"
      aria-hidden="true"
      focusable="false"
    >
      <path
        d="M0 178Q140 130 280 161T680 153V190H0Z"
        fill="#7adacb"
        opacity=".5"
      />

      <g fill="#4dbfb3" opacity=".36">
        <rect
          x="65"
          y="83"
          width="53"
          height="95"
          rx="3"
        />
        <rect
          x="131"
          y="58"
          width="41"
          height="120"
          rx="3"
        />
        <rect
          x="190"
          y="99"
          width="63"
          height="79"
          rx="3"
        />
        <rect
          x="476"
          y="76"
          width="56"
          height="102"
          rx="3"
        />
        <rect
          x="543"
          y="54"
          width="48"
          height="124"
          rx="3"
        />
        <rect
          x="605"
          y="92"
          width="47"
          height="86"
          rx="3"
        />
      </g>

      <g fill="#eafcf7" opacity=".7">
        {[
          84,
          104,
          147,
          210,
          229,
          492,
          513,
          558,
          577,
          622,
          639,
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

      <g>
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
      </g>

      <g fill="#27a98b">
        <circle cx="259" cy="132" r="28" />
        <circle cx="234" cy="144" r="21" />
        <circle cx="506" cy="134" r="29" />
        <circle cx="531" cy="146" r="22" />
      </g>
    </svg>
  );
}

function PageShell({
  children,
}: {
  children: ReactNode;
}) {
  const { lang, copy } = useLanguage();
  const { user, signOut } = useAuth();

  const navigate = useNavigate();
  const location = useLocation();

  const [theme, setTheme] =
    useState<Theme>(savedTheme);

  const [profileOpen, setProfileOpen] =
    useState(false);

  const [mobileOpen, setMobileOpen] =
    useState(false);

  const profileRef =
    useRef<HTMLDivElement>(null);

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    document.documentElement.style.colorScheme = theme;

    try {
      localStorage.setItem(
        "jonoseba-theme",
        theme,
      );
    } catch {
      // Theme works without storage.
    }
  }, [theme]);

  useEffect(() => {
    setProfileOpen(false);
    setMobileOpen(false);
    window.scrollTo(0, 0);
  }, [location.pathname]);

  useEffect(() => {
    const outside = (event: PointerEvent) => {
      if (
        profileRef.current &&
        !profileRef.current.contains(
          event.target as Node,
        )
      ) {
        setProfileOpen(false);
      }
    };

    const escape = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setProfileOpen(false);
      }
    };

    document.addEventListener(
      "pointerdown",
      outside,
    );

    document.addEventListener(
      "keydown",
      escape,
    );

    return () => {
      document.removeEventListener(
        "pointerdown",
        outside,
      );

      document.removeEventListener(
        "keydown",
        escape,
      );
    };
  }, []);

  const nav = [
    {
      to: "/",
      label: copy.home,
      end: true,
    },
    {
      to: "/services",
      label: copy.services,
      end: false,
    },
    {
      to: "/how-it-works",
      label: copy.how,
      end: true,
    },
    {
      to: "/ai-assistant",
      label: copy.ai,
      end: true,
    },
    {
      to: "/about",
      label: copy.about,
      end: true,
    },
  ];

  const initials =
    user?.full_name
      .trim()
      .split(/\s+/)
      .slice(0, 2)
      .map((p) => p[0])
      .join("")
      .toUpperCase() || "JS";

  return (
    <div className="jd-app">
      <header className="jd-header">
        <div className="jd-header-inner">
          <Link
            to="/dashboard"
            className="jd-brand"
            aria-label="JonoSeba dashboard"
          >
            <span className="jd-brand-symbol">
              <Landmark size={23} />
            </span>

            <span>
              <strong>জনসেবা</strong>
              <small>JONOSEBA</small>
            </span>
          </Link>

          <nav
            className={`jd-nav ${
              mobileOpen ? "jd-nav-open" : ""
            }`}
            aria-label="Dashboard navigation"
          >
            {nav.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.end}
                className={({ isActive }) =>
                  isActive
                    ? "jd-nav-link jd-nav-active"
                    : "jd-nav-link"
                }
              >
                {item.label}
              </NavLink>
            ))}

            <NavLink
              to="/dashboard"
              className="jd-nav-link"
            >
              {copy.dashboard}
            </NavLink>
          </nav>

          <div className="jd-header-actions">
            <div
              className="jd-language"
              role="group"
              aria-label="Language"
            >
              <Languages size={16} />

              <button
                type="button"
                className={
                  lang === "bn"
                    ? "jd-selected"
                    : ""
                }
                onClick={() =>
                  void changeAppLanguage("bn")
                }
                aria-pressed={lang === "bn"}
              >
                বাংলা
              </button>

              <span>/</span>

              <button
                type="button"
                className={
                  lang === "en"
                    ? "jd-selected"
                    : ""
                }
                onClick={() =>
                  void changeAppLanguage("en")
                }
                aria-pressed={lang === "en"}
              >
                EN
              </button>
            </div>

            <button
              className="jd-icon-btn"
              type="button"
              aria-label={copy.theme}
              onClick={() =>
                setTheme((value) =>
                  value === "dark"
                    ? "light"
                    : "dark"
                )
              }
            >
              {theme === "light" ? (
                <Moon size={19} />
              ) : (
                <Sun size={19} />
              )}
            </button>

            <div
              className="jd-profile-wrap"
              ref={profileRef}
            >
              <button
                className="jd-profile-trigger"
                type="button"
                aria-expanded={profileOpen}
                onClick={() =>
                  setProfileOpen(
                    (open) => !open,
                  )
                }
              >
                <span className="jd-avatar">
                  {initials}
                </span>

                <span className="jd-profile-name">
                  {user?.full_name}
                </span>

                <ChevronDown size={16} />
              </button>

              {profileOpen && (
                <div className="jd-profile-menu">
                  <Link to="/dashboard/profile">
                    <UserRound size={17} />
                    {copy.profile}
                  </Link>

                  <Link to="/dashboard/profile">
                    <Settings2 size={17} />
                    {copy.editProfile}
                  </Link>

                  <button
                    className="jd-logout"
                    type="button"
                    onClick={() => {
                      signOut();

                      navigate("/login", {
                        replace: true,
                      });
                    }}
                  >
                    <LogOut size={17} />
                    {copy.logout}
                  </button>
                </div>
              )}
            </div>

            <button
              className="jd-mobile-btn"
              type="button"
              aria-label={copy.menu}
              aria-expanded={mobileOpen}
              onClick={() =>
                setMobileOpen(
                  (open) => !open,
                )
              }
            >
              {mobileOpen ? (
                <X size={22} />
              ) : (
                <Menu size={22} />
              )}
            </button>
          </div>
        </div>
      </header>

      <main className="jd-main">
        {children}
      </main>

      <footer className="jd-footer">
        © {new Date().getFullYear()} JonoSeba ·{" "}
        {copy.demo}
      </footer>
    </div>
  );
}

function StatusBadge({
  status,
}: {
  status: ComplaintStatus;
}) {
  const { copy } = useLanguage();

  return (
    <span
      className={`jd-status jd-status-${status}`}
    >
      {copy.statuses[status]}
    </span>
  );
}

function ComplaintDetails({
  complaint,
  departments,
}: {
  complaint: Complaint;
  departments: Department[];
}) {
  const { copy, lang } = useLanguage();

  const department = departments.find(
    (d) => d.id === complaint.department_id,
  );

  const rows: {
    label: string;
    value: ReactNode;
  }[] = [
    {
      label: copy.status,
      value: (
        <StatusBadge status={complaint.status} />
      ),
    },
    {
      label: copy.department,
      value:
        department?.name ??
        `#${complaint.department_id}`,
    },
    {
      label: copy.priority,
      value: complaint.priority,
    },
    {
      label: copy.location,
      value: complaint.location,
    },
    {
      label: copy.created,
      value: readableDate(
        complaint.created_at,
        lang,
      ),
    },
    {
      label: copy.updated,
      value: readableDate(
        complaint.updated_at,
        lang,
      ),
    },
    {
      label: copy.description,
      value: complaint.description,
    },
  ];

  return (
    <div className="jd-record-detail">
      <h3>
        #{complaint.id} — {complaint.title}
      </h3>

      <dl>
        {rows.map((row) => (
          <div key={row.label}>
            <dt>{row.label}</dt>
            <dd>{row.value}</dd>
          </div>
        ))}
      </dl>

      <p className="jd-muted">
        {copy.noHistory}
      </p>
    </div>
  );
}

function ErrorState({
  error,
  retry,
}: {
  error: string;
  retry?: () => void;
}) {
  const { copy } = useLanguage();

  return (
    <div
      className="jd-feedback jd-feedback-error"
      role="alert"
    >
      <p>{error}</p>

      {retry && (
        <button
          type="button"
          className="jd-secondary-btn"
          onClick={retry}
        >
          <RefreshCw size={15} />
          {copy.retry}
        </button>
      )}
    </div>
  );
}

function ActionTile({
  to,
  title,
  description,
  Icon,
  tone,
  onClick,
}: {
  to?: string;
  title: string;
  description: string;
  Icon: LucideIcon;
  tone: string;
  onClick?: () => void;
}) {
  const content = (
    <>
      <span className="jd-action-icon">
        <Icon size={26} />
      </span>

      <span className="jd-action-text">
        <strong>{title}</strong>
        <small>{description}</small>
      </span>

      <ArrowRight size={19} />
    </>
  );

  const className =
    `jd-action jd-action-${tone}`;

  return to ? (
    <Link
      to={to}
      className={className}
    >
      {content}
    </Link>
  ) : (
    <button
      type="button"
      className={className}
      onClick={onClick}
    >
      {content}
    </button>
  );
}

function ChatPanel({
  onClose,
}: {
  onClose: () => void;
}) {
  const { copy } = useLanguage();

  const [question, setQuestion] = useState("");

  const [messages, setMessages] = useState<
    ChatHistoryMessage[]
  >([]);

  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const bottom = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottom.current?.scrollIntoView({
      behavior: "smooth",
      block: "nearest",
    });
  }, [messages, busy]);

  async function handleSend(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    const message = question.trim();

    if (!message || busy) {
      return;
    }

    setBusy(true);
    setError("");

    try {
      const answer = await askJonoSeba(
        message,
        messages.slice(-20),
      );

      setMessages((previous) => [
        ...previous,
        {
          role: "user",
          content: message,
        },
        {
          role: "model",
          content: answer.reply,
        },
      ]);

      setQuestion("");
    } catch (reason) {
      setError(friendlyError(reason));
    } finally {
      setBusy(false);
    }
  }

  return (
    <aside
      className="jd-chat"
      aria-label={copy.chatTitle}
    >
      <div className="jd-chat-header">
        <span className="jd-chat-logo">
          <Sparkles size={21} />
        </span>

        <div>
          <strong>{copy.chatTitle}</strong>

          <small>
            <span className="jd-online-dot" />
            {copy.chatPending}
          </small>
        </div>

        <button
          type="button"
          className="jd-chat-close"
          onClick={onClose}
          aria-label={copy.closeChat}
        >
          <X size={19} />
        </button>
      </div>

      <div
        className="jd-chat-body jd-chat-body-live"
        aria-live="polite"
      >
        {messages.length === 0 && (
          <div className="jd-chat-start">
            <span className="jd-chat-illustration">
              <Bot size={35} />
            </span>

            <h3>{copy.chatTitle}</h3>
            <p>{copy.chatWelcome}</p>
          </div>
        )}

        {messages.map((m, index) => (
          <div
            key={index}
            className={`jd-chat-bubble ${
              m.role === "user"
                ? "jd-chat-bubble-user"
                : "jd-chat-bubble-model"
            }`}
          >
            {m.content}
          </div>
        ))}

        {busy && (
          <p
            className="jd-muted"
            role="status"
          >
            {copy.chatBusy}
          </p>
        )}

        {error && (
          <ErrorState error={error} />
        )}

        <div ref={bottom} />
      </div>

      <form
        className="jd-chat-compose"
        onSubmit={(event) =>
          void handleSend(event)
        }
      >
        <label
          htmlFor="jd-chat-question"
          className="jd-visually-hidden"
        >
          {copy.chatInput}
        </label>

        <textarea
          id="jd-chat-question"
          rows={2}
          value={question}
          maxLength={5000}
          placeholder={copy.chatInput}
          onChange={(event) =>
            setQuestion(event.target.value)
          }
        />

        <button
          type="submit"
          aria-label={copy.chatSend}
          disabled={busy || !question.trim()}
        >
          <Send size={20} />
        </button>
      </form>
    </aside>
  );
}

function HomeDashboard() {
  const { user } = useAuth();
  const { copy, lang } = useLanguage();

  const {
    items,
    loading,
    error,
    refresh,
  } = useComplaintRecords(user?.id);

  const [chatOpen, setChatOpen] = useState(
    () =>
      window.matchMedia(
        "(min-width: 961px)",
      ).matches,
  );

  const stats = [
    {
      label: copy.total,
      value: items.length,
      Icon: ClipboardList,
      type: "teal",
    },
    {
      label: copy.progress,
      value: items.filter(
        (r) => r.status === "in_progress",
      ).length,
      Icon: Search,
      type: "blue",
    },
    {
      label: copy.resolved,
      value: items.filter(
        (r) => r.status === "resolved",
      ).length,
      Icon: CheckCircle2,
      type: "green",
    },
  ];

  return (
    <>
      <section className="jd-welcome">
        <div className="jd-welcome-text">
          <span className="jd-kicker">
            JONOSEBA CITIZEN PORTAL
          </span>

          <h1>
            {copy.welcome},{" "}
            {user?.full_name}!{" "}
            <span aria-hidden="true">👋</span>
          </h1>

          <p>{copy.welcomeText}</p>
        </div>

        <DashboardSkyline />
      </section>

      <div
        className={`jd-workspace ${
          chatOpen
            ? "jd-workspace-chat"
            : ""
        }`}
      >
        <div className="jd-workspace-main">
          <section
            className="jd-stats jd-stats-three"
            aria-label="Complaint statistics"
          >
            {stats.map((stat) => (
              <div
                key={stat.type}
                className={`jd-stat jd-stat-${stat.type}`}
              >
                <span className="jd-stat-icon">
                  <stat.Icon size={22} />
                </span>

                <div>
                  <span className="jd-stat-label">
                    {stat.label}
                  </span>

                  <strong>
                    {loading || error
                      ? "—"
                      : stat.value}
                  </strong>

                  {loading && (
                    <small>{copy.loading}</small>
                  )}
                </div>
              </div>
            ))}
          </section>

          {error && (
            <ErrorState
              error={error}
              retry={refresh}
            />
          )}

          <section
            className="jd-actions"
            aria-label="Quick actions"
          >
            <ActionTile
              to="/dashboard/complaints/new"
              Icon={FilePlus2}
              tone="primary"
              title={copy.newComplaint}
              description={copy.newDesc}
            />

            <ActionTile
              to="/dashboard/complaints/track"
              Icon={Search}
              tone="mint"
              title={copy.track}
              description={copy.trackDesc}
            />

            <ActionTile
              to="/services"
              Icon={LayoutGrid}
              tone="soft"
              title={copy.explore}
              description={copy.exploreDesc}
            />

            <ActionTile
              Icon={Sparkles}
              tone="lavender"
              title={copy.ask}
              description={copy.askDesc}
              onClick={() => setChatOpen(true)}
            />
          </section>

          <div className="jd-panels">
            <section className="jd-card jd-recent">
              <div className="jd-card-head">
                <h2>
                  <ClipboardList size={20} />
                  {copy.recent}
                </h2>

                <Link to="/dashboard/complaints">
                  {copy.viewAll}
                  <ArrowRight size={16} />
                </Link>
              </div>

              {loading ? (
                <p className="jd-muted">
                  {copy.loading}
                </p>
              ) : items.length ? (
                <div className="jd-record-list">
                  {items.slice(0, 4).map((item) => (
                    <Link
                      key={item.id}
                      to={`/dashboard/complaints/track?id=${item.id}`}
                      className="jd-record-row"
                    >
                      <div>
                        <strong>
                          #{item.id} · {item.title}
                        </strong>

                        <small>
                          {readableDate(
                            item.created_at,
                            lang,
                          )}
                        </small>
                      </div>

                      <StatusBadge
                        status={item.status}
                      />
                    </Link>
                  ))}
                </div>
              ) : (
                <div className="jd-empty-records">
                  <ClipboardList size={31} />
                  <p>{copy.noRecords}</p>
                </div>
              )}
            </section>

            <section className="jd-card jd-tracking">
              <div className="jd-card-head">
                <h2>
                  <MapPin size={21} />
                  {copy.tracking}
                </h2>

                <Link to="/dashboard/complaints/track">
                  {copy.viewAll}
                  <ArrowRight size={16} />
                </Link>
              </div>

              {items[0] ? (
                <div className="jd-record-detail">
                  <h3>
                    #{items[0].id} —{" "}
                    {items[0].title}
                  </h3>

                  <p>
                    <StatusBadge
                      status={items[0].status}
                    />
                  </p>

                  <p className="jd-muted">
                    {copy.updated}:{" "}
                    {readableDate(
                      items[0].updated_at,
                      lang,
                    )}
                  </p>

                  <p className="jd-muted">
                    {copy.noHistory}
                  </p>
                </div>
              ) : (
                <p className="jd-muted">
                  {copy.trackingEmpty}
                </p>
              )}
            </section>
          </div>

          <section className="jd-card jd-shortcuts">
            <div className="jd-card-head">
              <div>
                <h2>
                  <LayoutGrid size={21} />
                  {copy.shortcuts}
                </h2>

                <p className="jd-muted">
                  {copy.shortcutsDesc}
                </p>
              </div>

              <Link to="/services">
                {copy.viewAll}
                <ArrowRight size={16} />
              </Link>
            </div>

            <div className="jd-service-grid">
              {quickServices.map((service) => (
                <Link
                  key={service.key}
                  className="jd-service-link"
                  to={service.route}
                >
                  <service.Icon size={29} />

                  <strong>
                    {copy[service.key]}
                  </strong>

                  <ArrowUpRight size={15} />
                </Link>
              ))}
            </div>
          </section>
        </div>

        {chatOpen && (
          <ChatPanel
            onClose={() =>
              setChatOpen(false)
            }
          />
        )}
      </div>

      <button
        className="jd-chat-fab"
        type="button"
        aria-expanded={chatOpen}
        aria-label={
          chatOpen
            ? copy.closeChat
            : copy.openChat
        }
        onClick={() =>
          setChatOpen(
            (open) => !open,
          )
        }
      >
        {chatOpen ? (
          <X size={25} />
        ) : (
          <MessageCircle size={26} />
        )}
      </button>
    </>
  );
}

function SectionPage({
  title,
  description,
  children,
}: {
  title: string;
  description: string;
  children: ReactNode;
}) {
  const { copy } = useLanguage();

  return (
    <div className="jd-section-page">
      <Link
        className="jd-back"
        to="/dashboard"
      >
        <ArrowLeft size={17} />
        {copy.backDashboard}
      </Link>

      <div className="jd-section-heading">
        <h1>{title}</h1>
        <p>{description}</p>
      </div>

      {children}
    </div>
  );
}

function NewComplaintPage() {
  const { user } = useAuth();
  const { copy, lang } = useLanguage();

  const storageKey =
    `jonoseba-complaint-draft-${user?.id ?? "guest"}`;

  const [draft, setDraft] = useState<
    ComplaintDraft
  >(() => {
    try {
      const value: unknown = JSON.parse(
        sessionStorage.getItem(storageKey) ||
          "null",
      );

      if (
        value &&
        typeof value === "object"
      ) {
        const saved =
          value as Record<string, unknown>;

        return {
          title:
            typeof saved.title === "string"
              ? saved.title
              : "",
          departmentId:
            typeof saved.departmentId ===
            "string"
              ? saved.departmentId
              : "",
          ward:
            typeof saved.ward === "string"
              ? saved.ward
              : "",
          location:
            typeof saved.location === "string"
              ? saved.location
              : "",
          description:
            typeof saved.description ===
            "string"
              ? saved.description
              : "",
        };
      }
    } catch {
      // Invalid local draft.
    }

    return emptyDraft;
  });

  const [departments, setDepartments] =
    useState<Department[]>([]);

  const [departmentLoading, setDepartmentLoading] =
    useState(true);

  const [departmentError, setDepartmentError] =
    useState("");

  const [revision, setRevision] = useState(0);
  const [submitting, setSubmitting] = useState(false);
  const [feedback, setFeedback] = useState("");

  const [receipt, setReceipt] =
    useState<Complaint | null>(null);

  useEffect(() => {
    let active = true;

    getActiveDepartments()
      .then((all) => {
        if (!active) {
          return;
        }

        if (!Array.isArray(all)) {
          throw new Error(
            "Unexpected department response.",
          );
        }

        setDepartments(
          all.filter(
            (department) =>
              department.is_active,
          ),
        );

        setDepartmentError("");
      })
      .catch((reason: unknown) => {
        if (active) {
          setDepartmentError(
            friendlyError(reason),
          );
        }
      })
      .finally(() => {
        if (active) {
          setDepartmentLoading(false);
        }
      });

    return () => {
      active = false;
    };
  }, [revision]);

  function setField(
    field: keyof ComplaintDraft,
    value: string,
  ) {
    setDraft((current) => ({
      ...current,
      [field]: value,
    }));

    setFeedback("");
    setReceipt(null);
  }

  function clear() {
    setDraft(emptyDraft);
    setReceipt(null);
    setFeedback("");

    try {
      sessionStorage.removeItem(storageKey);
    } catch {
      // Storage unavailable.
    }
  }

  function saveDraft() {
    try {
      sessionStorage.setItem(
        storageKey,
        JSON.stringify(draft),
      );

      setFeedback(copy.draftSaved);
    } catch {
      setFeedback(
        lang === "bn"
          ? "খসড়া সংরক্ষণ করা যায়নি।"
          : "Could not save the draft.",
      );
    }
  }

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setFeedback("");
    setReceipt(null);

    const departmentId = Number(
      draft.departmentId,
    );

    if (
      !departments.some(
        (item) => item.id === departmentId,
      )
    ) {
      setFeedback(copy.chooseDepartment);
      return;
    }

    const location = draft.ward.trim()
      ? `Ward ${draft.ward.trim()}, ${draft.location.trim()}`
      : draft.location.trim();

    if (location.length > 255) {
      setFeedback(
        lang === "bn"
          ? "ঠিকানা ২৫৫ অক্ষরের বেশি হয়েছে।"
          : "Combined location must be at most 255 characters.",
      );

      return;
    }

    setSubmitting(true);

    try {
      const result = await submitComplaint({
        title: draft.title.trim(),
        description: draft.description.trim(),
        location,
        department_id: departmentId,
      });

      if (
        result.citizen_id !== user?.id
      ) {
        throw new Error(
          "Unexpected complaint owner returned by the server.",
        );
      }

      setReceipt(result);
      setDraft(emptyDraft);

      try {
        sessionStorage.removeItem(storageKey);
      } catch {
        // Continue after successful backend submission.
      }
    } catch (reason) {
      setFeedback(
        friendlyError(reason),
      );
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <SectionPage
      title={copy.complaintNewTitle}
      description={copy.complaintNewDesc}
    >
      {receipt && (
        <div
          className="jd-feedback jd-feedback-success"
          role="status"
        >
          <strong>{copy.submitted}</strong>

          <p>
            {copy.receipt}:{" "}
            <strong>#{receipt.id}</strong>
          </p>

          <Link
            className="jd-primary-btn"
            to={`/dashboard/complaints/track?id=${receipt.id}`}
          >
            {copy.viewStatus}
            <ArrowRight size={16} />
          </Link>
        </div>
      )}

      <form
        className="jd-form jd-card"
        onSubmit={(event) =>
          void handleSubmit(event)
        }
      >
        <div className="jd-form-grid">
          <label>
            {copy.labelTitle}

            <input
              required
              minLength={5}
              maxLength={200}
              value={draft.title}
              onChange={(event) =>
                setField(
                  "title",
                  event.target.value,
                )
              }
            />
          </label>

          <label>
            {copy.labelDepartment}

            <select
              required
              value={draft.departmentId}
              disabled={
                departmentLoading ||
                !!departmentError ||
                !departments.length
              }
              onChange={(event) =>
                setField(
                  "departmentId",
                  event.target.value,
                )
              }
            >
              <option value="">
                {copy.chooseDepartment}
              </option>

              {departments.map(
                (department) => (
                  <option
                    key={department.id}
                    value={department.id}
                  >
                    {department.name}
                  </option>
                ),
              )}
            </select>
          </label>
        </div>

        {departmentLoading && (
          <p className="jd-muted">
            {copy.loading}
          </p>
        )}

        {departmentError && (
          <ErrorState
            error={departmentError}
            retry={() => {
              setDepartmentLoading(true);
              setRevision((n) => n + 1);
            }}
          />
        )}

        {!departmentLoading &&
          !departmentError &&
          !departments.length && (
            <p className="jd-feedback jd-feedback-error">
              {copy.noDepartments}
            </p>
          )}

        <div className="jd-form-grid">
          <label>
            {copy.labelWard}

            <input
              maxLength={40}
              value={draft.ward}
              onChange={(event) =>
                setField(
                  "ward",
                  event.target.value,
                )
              }
            />
          </label>

          <label>
            {copy.labelLocation}

            <input
              required
              minLength={3}
              maxLength={255}
              value={draft.location}
              onChange={(event) =>
                setField(
                  "location",
                  event.target.value,
                )
              }
            />
          </label>
        </div>

        <p className="jd-muted">
          {copy.locationNote}
        </p>

        <label>
          {copy.labelDescription}

          <textarea
            required
            minLength={10}
            maxLength={5000}
            rows={6}
            value={draft.description}
            onChange={(event) =>
              setField(
                "description",
                event.target.value,
              )
            }
          />
        </label>

        {feedback && (
          <p
            className="jd-feedback jd-feedback-error"
            role="alert"
          >
            {feedback}
          </p>
        )}

        <div className="jd-form-actions">
          <button
            className="jd-secondary-btn"
            type="button"
            onClick={clear}
          >
            {copy.draftClear}
          </button>

          <button
            className="jd-secondary-btn"
            type="button"
            onClick={saveDraft}
          >
            <Bookmark size={17} />
            {copy.draftSave}
          </button>

          <button
            className="jd-primary-btn"
            type="submit"
            disabled={
              submitting ||
              departmentLoading ||
              !!departmentError ||
              !departments.length
            }
          >
            <FilePlus2 size={17} />
            {submitting
              ? copy.submitting
              : copy.submit}
          </button>
        </div>
      </form>
    </SectionPage>
  );
}

function ComplaintsPage() {
  const { user } = useAuth();
  const { copy, lang } = useLanguage();

  const {
    items,
    loading,
    error,
    refresh,
  } = useComplaintRecords(user?.id);

  return (
    <SectionPage
      title={copy.complaintPage}
      description={copy.complaintPageDesc}
    >
      <div className="jd-card">
        {loading && (
          <p className="jd-muted">
            {copy.loading}
          </p>
        )}

        {error && (
          <ErrorState
            error={error}
            retry={refresh}
          />
        )}

        {!loading &&
          !error &&
          (items.length ? (
            <div className="jd-record-list">
              {items.map((item) => (
                <Link
                  key={item.id}
                  className="jd-record-row"
                  to={`/dashboard/complaints/track?id=${item.id}`}
                >
                  <div>
                    <strong>
                      #{item.id} — {item.title}
                    </strong>

                    <small>
                      {item.location} ·{" "}
                      {readableDate(
                        item.created_at,
                        lang,
                      )}
                    </small>
                  </div>

                  <StatusBadge
                    status={item.status}
                  />
                </Link>
              ))}
            </div>
          ) : (
            <p className="jd-muted">
              {copy.noRecords}
            </p>
          ))}

        <div className="jd-form-actions">
          <Link
            className="jd-primary-btn"
            to="/dashboard/complaints/new"
          >
            <FilePlus2 size={18} />
            {copy.newComplaint}
          </Link>
        </div>
      </div>
    </SectionPage>
  );
}

function TrackPage() {
  const { user } = useAuth();
  const { copy } = useLanguage();
  const [params] = useSearchParams();

  const initialId =
    params.get("id") || "";

  const [query, setQuery] =
    useState(initialId);

  const [complaint, setComplaint] =
    useState<Complaint | null>(null);

  const [departments, setDepartments] =
    useState<Department[]>([]);

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let active = true;

    getActiveDepartments()
      .then((items) => {
        if (
          active &&
          Array.isArray(items)
        ) {
          setDepartments(items);
        }
      })
      .catch(() => {
        // Department ID is shown if names cannot load.
      });

    return () => {
      active = false;
    };
  }, []);

  async function searchFor(value: string) {
    const id = Number(value);

    setComplaint(null);
    setError("");

    if (
      !/^\d+$/.test(value.trim()) ||
      !Number.isSafeInteger(id) ||
      id < 1
    ) {
      setError(copy.invalidId);
      return;
    }

    setLoading(true);

    try {
      const item =
        await getComplaintById(id);

      if (
        item.citizen_id !== user?.id
      ) {
        throw new Error(copy.notOwned);
      }

      setComplaint(item);
    } catch (reason) {
      setError(friendlyError(reason));
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (initialId) {
      void searchFor(initialId);
    }

    // Search when URL complaint ID changes.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [initialId]);

  return (
    <SectionPage
      title={copy.trackPage}
      description={copy.trackPageDesc}
    >
      <div className="jd-card jd-tracking-search">
        <form
          onSubmit={(event) => {
            event.preventDefault();
            void searchFor(query);
          }}
        >
          <label htmlFor="jd-track-id">
            {copy.searchPlaceholder}
          </label>

          <div className="jd-track-controls">
            <input
              id="jd-track-id"
              inputMode="numeric"
              value={query}
              onChange={(event) =>
                setQuery(event.target.value)
              }
              placeholder={
                copy.searchPlaceholder
              }
            />

            <button
              type="submit"
              className="jd-primary-btn"
              disabled={loading}
            >
              <Search size={17} />
              {copy.find}
            </button>
          </div>
        </form>

        {loading && (
          <p className="jd-muted">
            {copy.loading}
          </p>
        )}

        {error && (
          <ErrorState error={error} />
        )}

        {complaint && (
          <ComplaintDetails
            complaint={complaint}
            departments={departments}
          />
        )}
      </div>
    </SectionPage>
  );
}

function ProfilePage() {
  const { user } = useAuth();
  const { copy } = useLanguage();

  return (
    <SectionPage
      title={copy.profileTitle}
      description={copy.profileDesc}
    >
      <div className="jd-card jd-profile-page">
        <span className="jd-profile-big">
          <UserRound size={34} />
        </span>

        <dl>
          <div>
            <dt>{copy.name}</dt>
            <dd>{user?.full_name}</dd>
          </div>

          <div>
            <dt>{copy.email}</dt>
            <dd>{user?.email}</dd>
          </div>

          <div>
            <dt>{copy.role}</dt>
            <dd>{user?.role}</dd>
          </div>

          <div>
            <dt>{copy.account}</dt>
            <dd>
              {user?.is_active
                ? copy.active
                : copy.inactive}
            </dd>
          </div>
        </dl>

        <p className="jd-form-warning">
          <ShieldCheck size={18} />
          {copy.editPending}
        </p>
      </div>
    </SectionPage>
  );
}

export default function DashboardPage({
  view = "home",
}: {
  view?: DashboardView;
}) {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div
        className="jd-loading"
        role="status"
      >
        Loading JonoSeba...
      </div>
    );
  }

  if (!user) {
    return (
      <Navigate to="/login" replace />
    );
  }

  const pages: Record<
    DashboardView,
    ReactNode
  > = {
    home: <HomeDashboard />,
    new: <NewComplaintPage />,
    complaints: <ComplaintsPage />,
    track: <TrackPage />,
    profile: <ProfilePage />,
  };

  return (
    <PageShell>
      {pages[view]}
    </PageShell>
  );
}
