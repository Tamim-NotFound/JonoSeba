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
  Lightbulb,
  ListFilter,
  LogOut,
  MapPin,
  Menu,
  MessageCircle,
  Moon,
  Search,
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

import "./dashboard.css";

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
  category: string;
  ward: string;
  location: string;
  description: string;
};

const emptyDraft: ComplaintDraft = {
  title: "",
  category: "",
  ward: "",
  location: "",
  description: "",
};

// All dashboard text in Bengali and English.
const words = {
  en: {
    home: "Home",
    services: "Services",
    how: "How it works",
    ai: "AI Assistant",
    about: "About",
    dashboard: "Dashboard",
    profile: "Profile",
    editProfile: "Edit profile (coming soon)",
    logout: "Logout",
    menu: "Open menu",
    theme: "Toggle dark or light mode",

    welcome: "Welcome back",
    welcomeText:
      "Your citizen-service workspace: report civic issues, track their progress, and explore municipal information.",

    demo: "Educational demo — not an official government portal",

    total: "Total complaints",
    pending: "Pending",
    progress: "In progress",
    resolved: "Resolved",
    saved: "Saved services",
    aiRequests: "AI requests",
    awaiting: "Awaiting API connection",

    newComplaint: "File new complaint",
    newDesc: "Describe an issue in your area",
    track: "Track complaint",
    trackDesc: "Check a complaint's progress",
    explore: "Explore services",
    exploreDesc: "Browse municipal guidance",
    ask: "Ask AI assistant",
    askDesc: "Open the chat panel",

    recent: "Recent complaints",
    viewAll: "View all",
    noRecords:
      "Your real complaint history will appear after the authorized complaint API is connected.",

    tracking: "Complaint tracking",
    trackingEmpty:
      "No complaint selected yet. Real progress and timestamps will come from the backend.",
    trackingStages: "Example stages (not live status)",
    submitted: "Submitted",
    review: "Under review",
    processing: "In progress",
    resolvedStage: "Resolved",

    shortcuts: "Service shortcuts",
    shortcutsDesc:
      "Discover the most-used municipal topics",

    water: "Water supply",
    lighting: "Street lighting",
    waste: "Waste management",
    health: "Health and environment",
    birth: "Birth & death registration",
    holding: "Holding tax",
    trade: "Trade license",

    chatTitle: "JonoSeba AI Assistant",
    chatPending: "Live chat connection pending",
    chatWelcome:
      "Your AI chat window is ready. Responses will appear here after the Gemini endpoint is connected.",
    chatInput: "Ask about services or complaints...",
    chatSend: "Send message",
    chatNotSent:
      "Your message was not sent. The AI backend endpoint must be connected first.",
    closeChat: "Close AI chat",
    openChat: "Open AI chat",
    chatStatus: "Not connected",

    complaintPage: "My complaints",
    complaintPageDesc:
      "Review your submitted municipal complaints once the API is connected.",

    complaintNewTitle: "New complaint",
    complaintNewDesc:
      "Prepare a complaint draft. Saving a draft does not submit it to the municipality.",

    labelTitle: "Complaint title",
    labelCategory: "Issue category",
    labelWard: "Ward / area",
    labelLocation: "Specific location",
    labelDescription: "Describe the problem",
    chooseCategory: "Choose a category",

    draftSaved:
      "Draft saved in this browser session only. No complaint was submitted.",
    draftClear: "Clear draft",
    draftSave: "Save local draft",
    submissionPending:
      "Submission will be enabled after backend schema integration.",

    profileTitle: "Your profile",
    profileDesc:
      "Information verified using your logged-in account.",
    name: "Full name",
    email: "Email",
    role: "Role",
    account: "Account status",
    active: "Active",
    inactive: "Inactive",
    editPending:
      "Profile editing needs a backend update endpoint. This page currently displays your real account details only.",

    trackPage: "Track a complaint",
    trackPageDesc:
      "Live tracking will use your authenticated complaint records.",
    searchPlaceholder: "Complaint ID or keyword",
    searchPending:
      "Search will become available once complaint retrieval is connected.",

    backDashboard: "Back to dashboard",
    noData: "—",
  },

  bn: {
    home: "হোম",
    services: "সেবাসমূহ",
    how: "যেভাবে কাজ করে",
    ai: "AI সহকারী",
    about: "সম্পর্কে",
    dashboard: "ড্যাশবোর্ড",
    profile: "প্রোফাইল",
    editProfile: "প্রোফাইল সম্পাদনা (শিগগিরই)",
    logout: "লগআউট",
    menu: "মেনু খুলুন",
    theme: "ডার্ক বা লাইট মোড",

    welcome: "স্বাগতম",
    welcomeText:
      "আপনার নাগরিক সেবার জায়গা—সমস্যার অভিযোগ প্রস্তুত করুন, অগ্রগতি দেখুন এবং পৌরসেবার তথ্য খুঁজুন।",

    demo: "শিক্ষামূলক ডেমো — সরকারি অনুমোদিত পোর্টাল নয়",

    total: "মোট অভিযোগ",
    pending: "অপেক্ষমাণ",
    progress: "চলমান",
    resolved: "সমাধান হয়েছে",
    saved: "সংরক্ষিত সেবা",
    aiRequests: "AI অনুরোধ",
    awaiting: "API সংযোগ বাকি",

    newComplaint: "নতুন অভিযোগ",
    newDesc: "আপনার এলাকার সমস্যার বিবরণ দিন",
    track: "অভিযোগ ট্র্যাক করুন",
    trackDesc: "অভিযোগের অগ্রগতি দেখুন",
    explore: "সেবা খুঁজুন",
    exploreDesc: "পৌরসেবার তথ্য দেখুন",
    ask: "AI সহায়তা নিন",
    askDesc: "চ্যাট প্যানেল খুলুন",

    recent: "সাম্প্রতিক অভিযোগ",
    viewAll: "সব দেখুন",
    noRecords:
      "নিরাপদ complaint API সংযুক্ত হলে আপনার প্রকৃত অভিযোগের তালিকা এখানে দেখা যাবে।",

    tracking: "অভিযোগের অগ্রগতি",
    trackingEmpty:
      "এখনো কোনো অভিযোগ নির্বাচন করা হয়নি। প্রকৃত অগ্রগতি ও সময় backend থেকে দেখানো হবে।",
    trackingStages: "সম্ভাব্য ধাপ (বর্তমান অবস্থা নয়)",
    submitted: "জমা হয়েছে",
    review: "যাচাই চলছে",
    processing: "কাজ চলছে",
    resolvedStage: "সমাধান",

    shortcuts: "প্রয়োজনীয় সেবা",
    shortcutsDesc: "জনপ্রিয় পৌরসেবার তথ্য দেখুন",

    water: "পানি সরবরাহ",
    lighting: "সড়কবাতি",
    waste: "বর্জ্য ব্যবস্থাপনা",
    health: "স্বাস্থ্য ও পরিবেশ",
    birth: "জন্ম ও মৃত্যু নিবন্ধন",
    holding: "হোল্ডিং ট্যাক্স",
    trade: "ট্রেড লাইসেন্স",

    chatTitle: "জনসেবা AI সহকারী",
    chatPending: "লাইভ চ্যাট সংযোগ বাকি",
    chatWelcome:
      "AI চ্যাটের ডিজাইন প্রস্তুত। Gemini endpoint যুক্ত হওয়ার পর এখানেই প্রকৃত উত্তর আসবে।",
    chatInput: "পৌরসেবা বা অভিযোগ নিয়ে প্রশ্ন লিখুন...",
    chatSend: "মেসেজ পাঠান",
    chatNotSent:
      "আপনার মেসেজ পাঠানো হয়নি। আগে AI backend endpoint সংযুক্ত করতে হবে।",
    closeChat: "AI চ্যাট বন্ধ করুন",
    openChat: "AI চ্যাট খুলুন",
    chatStatus: "সংযোগ নেই",

    complaintPage: "আমার অভিযোগসমূহ",
    complaintPageDesc:
      "Backend সংযুক্ত হলে আপনার নিজের জমা দেওয়া অভিযোগ এখানে দেখা যাবে।",

    complaintNewTitle: "নতুন অভিযোগ",
    complaintNewDesc:
      "অভিযোগের খসড়া তৈরি করুন। খসড়া সংরক্ষণ মানে পৌরসভায় অভিযোগ জমা নয়।",

    labelTitle: "অভিযোগের শিরোনাম",
    labelCategory: "সমস্যার ধরন",
    labelWard: "ওয়ার্ড / এলাকা",
    labelLocation: "সুনির্দিষ্ট স্থান",
    labelDescription: "সমস্যার বিবরণ",
    chooseCategory: "ধরন নির্বাচন করুন",

    draftSaved:
      "এই ব্রাউজার সেশনে খসড়া সংরক্ষিত হয়েছে। কোনো অভিযোগ জমা হয়নি।",
    draftClear: "খসড়া মুছুন",
    draftSave: "খসড়া সংরক্ষণ",
    submissionPending:
      "Backend schema যুক্ত হলে অভিযোগ জমা দেওয়ার সুবিধা চালু হবে।",

    profileTitle: "আপনার প্রোফাইল",
    profileDesc:
      "লগইন করা অ্যাকাউন্ট থেকে পাওয়া প্রকৃত তথ্য।",
    name: "পুরো নাম",
    email: "ইমেইল",
    role: "ভূমিকা",
    account: "অ্যাকাউন্টের অবস্থা",
    active: "সক্রিয়",
    inactive: "নিষ্ক্রিয়",
    editPending:
      "প্রোফাইল পরিবর্তনের জন্য backend update endpoint দরকার। আপাতত এখানে আপনার প্রকৃত তথ্য দেখানো হচ্ছে।",

    trackPage: "অভিযোগ ট্র্যাক করুন",
    trackPageDesc:
      "লগইন করা ব্যবহারকারীর প্রকৃত অভিযোগ থেকে অগ্রগতি দেখানো হবে।",
    searchPlaceholder: "অভিযোগের ID বা শব্দ",
    searchPending:
      "Complaint retrieval সংযুক্ত হলে সার্চ চালু হবে।",

    backDashboard: "ড্যাশবোর্ডে ফিরুন",
    noData: "—",
  },
} as const;

function savedTheme(): Theme {
  try {
    return localStorage.getItem("jonoseba-theme") === "dark"
      ? "dark"
      : "light";
  } catch {
    return "light";
  }
}

function useLanguage() {
  const { i18n } = useTranslation();

  const lang: Language =
    i18n.resolvedLanguage === "en" ? "en" : "bn";

  return {
    lang,
    copy: words[lang],
  };
}

const quickServices: {
  key: "water" | "lighting" | "waste" | "birth" | "holding" | "trade";
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
    Icon: Lightbulb,
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

        {/* Bangladesh national flag: green field and red circle */}
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
          fill="#07675f"
          fontWeight="bold"
        >
        
          
          আপনার{" "}
          <tspan fill="#DC2626">শহর</tspan>
          {", আপনার "}
          <tspan fill="#DC2626">সেবা</tspan>
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

  const [theme, setTheme] = useState<Theme>(savedTheme);
  const [profileOpen, setProfileOpen] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  const profileRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    document.documentElement.style.colorScheme = theme;

    try {
      localStorage.setItem("jonoseba-theme", theme);
    } catch {
      // Theme continues to work without local storage.
    }
  }, [theme]);

  useEffect(() => {
    setProfileOpen(false);
    setMobileOpen(false);
    window.scrollTo(0, 0);
  }, [location.pathname]);

  useEffect(() => {
    function handlePointerDown(event: PointerEvent) {
      if (
        profileRef.current &&
        !profileRef.current.contains(
          event.target as Node
        )
      ) {
        setProfileOpen(false);
      }
    }

    function handleKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") {
        setProfileOpen(false);
      }
    }

    document.addEventListener(
      "pointerdown",
      handlePointerDown
    );

    document.addEventListener(
      "keydown",
      handleKeyDown
    );

    return () => {
      document.removeEventListener(
        "pointerdown",
        handlePointerDown
      );

      document.removeEventListener(
        "keydown",
        handleKeyDown
      );
    };
  }, []);

  function logout() {
    signOut();
    navigate("/login", { replace: true });
  }

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
      .map((part) => part[0])
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
                  lang === "bn" ? "jd-selected" : ""
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
                  lang === "en" ? "jd-selected" : ""
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
              title={copy.theme}
              onClick={() =>
                setTheme((previous) =>
                  previous === "light"
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

            <div
              className="jd-profile-wrap"
              ref={profileRef}
            >
              <button
                className="jd-profile-trigger"
                type="button"
                aria-expanded={profileOpen}
                aria-haspopup="menu"
                onClick={() =>
                  setProfileOpen((open) => !open)
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
                <div
                  className="jd-profile-menu"
                  role="menu"
                >
                  <Link
                    role="menuitem"
                    to="/dashboard/profile"
                  >
                    <UserRound size={17} />
                    {copy.profile}
                  </Link>

                  <Link
                    role="menuitem"
                    to="/dashboard/profile"
                  >
                    <Settings2 size={17} />
                    {copy.editProfile}
                  </Link>

                  <button
                    role="menuitem"
                    type="button"
                    onClick={logout}
                    className="jd-logout"
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
                setMobileOpen((value) => !value)
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
        © {new Date().getFullYear()} JonoSeba · {copy.demo}
      </footer>
    </div>
  );
}

function Statistic({
  label,
  Icon,
  type,
}: {
  label: string;
  Icon: LucideIcon;
  type: string;
}) {
  const { copy } = useLanguage();

  return (
    <div className={`jd-stat jd-stat-${type}`}>
      <span className="jd-stat-icon">
        <Icon size={22} />
      </span>

      <div>
        <span className="jd-stat-label">
          {label}
        </span>

        <strong>{copy.noData}</strong>

        <small>{copy.awaiting}</small>
      </div>
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
  const contents = (
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

  const className = `jd-action jd-action-${tone}`;

  if (to) {
    return (
      <Link
        to={to}
        className={className}
      >
        {contents}
      </Link>
    );
  }

  return (
    <button
      type="button"
      className={className}
      onClick={onClick}
    >
      {contents}
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
  const [notice, setNotice] = useState(false);

  function handleSend(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    if (!question.trim()) {
      return;
    }

    // The AI API has not been connected yet.
    // Do not pretend that a message was sent.
    setNotice(true);
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
            <span className="jd-offline-dot" />
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

      <div className="jd-chat-body">
        <div className="jd-chat-illustration">
          <Bot size={35} />
        </div>

        <h3>{copy.chatTitle}</h3>
        <p>{copy.chatWelcome}</p>

        <span className="jd-chat-state">
          {copy.chatStatus}
        </span>

        {notice && (
          <p
            className="jd-chat-notice"
            role="alert"
          >
            {copy.chatNotSent}
          </p>
        )}
      </div>

      <form
        className="jd-chat-compose"
        onSubmit={handleSend}
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
          maxLength={2000}
          placeholder={copy.chatInput}
          onChange={(event) => {
            setQuestion(event.target.value);
            setNotice(false);
          }}
        />

        <button
          type="submit"
          aria-label={copy.chatSend}
          title={copy.chatSend}
        >
          <ArrowRight size={20} />
        </button>
      </form>
    </aside>
  );
}

function HomeDashboard() {
  const { user } = useAuth();
  const { copy } = useLanguage();

  const [chatOpen, setChatOpen] = useState(
    () =>
      typeof window !== "undefined" &&
      window.matchMedia("(min-width: 961px)").matches
  );

  const stats: {
    label: string;
    Icon: LucideIcon;
    type: string;
  }[] = [
    {
      label: copy.total,
      Icon: ClipboardList,
      type: "teal",
    },
    {
      label: copy.progress,
      Icon: Search,
      type: "blue",
    },
    {
      label: copy.resolved,
      Icon: CheckCircle2,
      type: "green",
    },
  ];

  const steps = [
    copy.submitted,
    copy.review,
    copy.processing,
    copy.resolvedStage,
  ];

  return (
    <>
      <section className="jd-welcome">
        <div className="jd-welcome-text">
          <span className="jd-kicker">
            JONOSEBA CITIZEN PORTAL
          </span>

          <h1>
            {copy.welcome}, {user?.full_name}!{" "}
            <span aria-hidden="true"></span>
          </h1>

          <p>{copy.welcomeText}</p>
        </div>

        <DashboardSkyline />
      </section>

      <div
        className={`jd-workspace ${
          chatOpen ? "jd-workspace-chat" : ""
        }`}
      >
        <div className="jd-workspace-main">
          <section
            className="jd-stats"
            aria-label="Complaint statistics"
            style={{
              gridTemplateColumns:
                "repeat(auto-fit, minmax(min(100%, 185px), 1fr))",
            }}
          >
            {stats.map((stat) => (
              <Statistic
                key={stat.type}
                {...stat}
              />
            ))}
          </section>

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

              <div className="jd-empty-records">
                <ClipboardList size={31} />
                <p>{copy.noRecords}</p>
              </div>
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

              <p className="jd-muted">
                {copy.trackingEmpty}
              </p>

              <span className="jd-section-note">
                {copy.trackingStages}
              </span>

              <ol className="jd-timeline">
                {steps.map((step) => (
                  <li key={step}>
                    <span className="jd-timeline-dot" />
                    <span>{step}</span>
                  </li>
                ))}
              </ol>
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
                  to={service.route}
                  className="jd-service-link"
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
            onClose={() => setChatOpen(false)}
          />
        )}
      </div>

      <button
        className="jd-chat-fab"
        type="button"
        aria-label={
          chatOpen
            ? copy.closeChat
            : copy.openChat
        }
        aria-expanded={chatOpen}
        onClick={() =>
          setChatOpen((current) => !current)
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
        to="/dashboard"
        className="jd-back"
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
  const { lang, copy } = useLanguage();

  const storageKey =
    `jonoseba-complaint-draft-${user?.id ?? "guest"}`;

  const [draft, setDraft] = useState<ComplaintDraft>(
    () => {
      try {
        const stored =
          sessionStorage.getItem(storageKey);

        if (stored) {
          const value: unknown = JSON.parse(stored);

          if (
            value &&
            typeof value === "object"
          ) {
            const data =
              value as Record<string, unknown>;

            const keys = [
              "title",
              "category",
              "ward",
              "location",
              "description",
            ];

            if (
              keys.every(
                (key) =>
                  typeof data[key] === "string"
              )
            ) {
              return {
                title: data.title as string,
                category: data.category as string,
                ward: data.ward as string,
                location: data.location as string,
                description: data.description as string,
              };
            }
          }
        }
      } catch {
        // Ignore unavailable or invalid browser storage.
      }

      return emptyDraft;
    }
  );

  const [message, setMessage] = useState("");

  const categories = [
    copy.water,
    copy.lighting,
    copy.waste,
    copy.health,
    copy.holding,
  ];

  function setField(
    key: keyof ComplaintDraft,
    value: string
  ) {
    setDraft((current) => ({
      ...current,
      [key]: value,
    }));

    setMessage("");
  }

  function save(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    try {
      sessionStorage.setItem(
        storageKey,
        JSON.stringify(draft)
      );

      setMessage(copy.draftSaved);
    } catch {
      setMessage(
        lang === "bn"
          ? "ব্রাউজারে খসড়া সংরক্ষণ করা যায়নি।"
          : "Could not save the draft in this browser."
      );
    }
  }

  function clear() {
    setDraft(emptyDraft);
    setMessage("");

    try {
      sessionStorage.removeItem(storageKey);
    } catch {
      // No action required.
    }
  }

  return (
    <SectionPage
      title={copy.complaintNewTitle}
      description={copy.complaintNewDesc}
    >
      <form
        className="jd-form jd-card"
        onSubmit={save}
      >
        <div className="jd-form-grid">
          <label>
            {copy.labelTitle}

            <input
              value={draft.title}
              onChange={(event) =>
                setField(
                  "title",
                  event.target.value
                )
              }
              maxLength={150}
              required
            />
          </label>

          <label>
            {copy.labelCategory}

            <select
              value={draft.category}
              onChange={(event) =>
                setField(
                  "category",
                  event.target.value
                )
              }
              required
            >
              <option value="">
                {copy.chooseCategory}
              </option>

              {categories.map((category) => (
                <option
                  key={category}
                  value={category}
                >
                  {category}
                </option>
              ))}
            </select>
          </label>
        </div>

        <div className="jd-form-grid">
          <label>
            {copy.labelWard}

            <input
              value={draft.ward}
              onChange={(event) =>
                setField(
                  "ward",
                  event.target.value
                )
              }
              maxLength={80}
              required
            />
          </label>

          <label>
            {copy.labelLocation}

            <input
              value={draft.location}
              onChange={(event) =>
                setField(
                  "location",
                  event.target.value
                )
              }
              maxLength={200}
              required
            />
          </label>
        </div>

        <label>
          {copy.labelDescription}

          <textarea
            value={draft.description}
            onChange={(event) =>
              setField(
                "description",
                event.target.value
              )
            }
            minLength={10}
            maxLength={3000}
            rows={6}
            required
          />
        </label>

        <p className="jd-form-warning">
          <ShieldCheck size={18} />
          {copy.submissionPending}
        </p>

        {message && (
          <p
            className="jd-draft-message"
            role="status"
          >
            {message}
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
            className="jd-primary-btn"
            type="submit"
          >
            <Bookmark size={17} />
            {copy.draftSave}
          </button>
        </div>
      </form>
    </SectionPage>
  );
}

function ComplaintsPage() {
  const { copy } = useLanguage();

  return (
    <SectionPage
      title={copy.complaintPage}
      description={copy.complaintPageDesc}
    >
      <div className="jd-card jd-list-empty">
        <ListFilter size={34} />

        <h2>{copy.awaiting}</h2>

        <p>{copy.noRecords}</p>

        <Link
          className="jd-primary-btn"
          to="/dashboard/complaints/new"
        >
          <FilePlus2 size={18} />
          {copy.newComplaint}
        </Link>
      </div>
    </SectionPage>
  );
}

function TrackPage() {
  const { copy } = useLanguage();

  return (
    <SectionPage
      title={copy.trackPage}
      description={copy.trackPageDesc}
    >
      <div className="jd-card jd-track-placeholder">
        <MapPin size={36} />

        <h2>{copy.awaiting}</h2>

        <p>{copy.searchPending}</p>

        <div className="jd-search-placeholder">
          <Search size={19} />

          <input
            placeholder={copy.searchPlaceholder}
            aria-label={copy.searchPlaceholder}
            disabled
          />
        </div>
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

  const pages: Record<DashboardView, ReactNode> = {
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
