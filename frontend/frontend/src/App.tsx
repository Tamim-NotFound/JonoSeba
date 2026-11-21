import { useEffect, useState, type ReactNode } from "react";
import {
  Link,
  NavLink,
  Route,
  Routes,
  useLocation,
  useParams,
} from "react-router-dom";
import { useTranslation } from "react-i18next";
import {
  ArrowRight,
  ArrowUpRight,
  BadgeCheck,
  Building2,
  CheckCircle2,
  ChevronRight,
  Droplets,
  FileText,
  HeartPulse,
  Landmark,
  Languages,
  LockKeyhole,
  Menu,
  MessageCircle,
  Moon,
  Search,
  ShieldCheck,
  Sparkles,
  Sun,
  X,
  type LucideIcon,
} from "lucide-react";

import { changeAppLanguage, type AppLanguage } from "./i18n";
import {
  services,
  siteCopy,
  type ServiceId,
  type SiteLanguage,
} from "./siteContent";

import "./index.css";

type Theme = "light" | "dark";

const serviceIcons: Record<ServiceId, LucideIcon> = {
  birth: FileText,
  trade: Building2,
  certificate: BadgeCheck,
  tax: Landmark,
  water: Droplets,
  health: HeartPulse,
};

function getSavedTheme(): Theme {
  try {
    return localStorage.getItem("jonoseba-theme") === "dark"
      ? "dark"
      : "light";
  } catch {
    return "light";
  }
}

function useSiteLanguage() {
  const { i18n } = useTranslation();

  const lang: SiteLanguage =
    i18n.resolvedLanguage === "en" ? "en" : "bn";

  return { lang, copy: siteCopy[lang] };
}

function ScrollToTop() {
  const { pathname } = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  return null;
}

function Logo() {
  return (
    <Link to="/" className="brand" aria-label="JonoSeba home">
      <span className="brand-icon">
        <Landmark size={25} />
      </span>
      <span className="brand-words">
        <strong>জনসেবা</strong>
        <small>JONOSEBA</small>
      </span>
    </Link>
  );
}

function Layout({ children }: { children: ReactNode }) {
  const { t } = useTranslation();
  const { lang, copy } = useSiteLanguage();
  const { pathname } = useLocation();

  const [theme, setTheme] = useState<Theme>(getSavedTheme);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    document.documentElement.style.colorScheme = theme;

    try {
      localStorage.setItem("jonoseba-theme", theme);
    } catch {
      // Theme still works when storage is unavailable.
    }
  }, [theme]);

  useEffect(() => {
    setMenuOpen(false);
  }, [pathname]);

  const navItems = [
    { path: "/", label: t("navHome"), end: true },
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
      label: lang === "bn" ? "সম্পর্কে" : "About",
      end: true,
    },
  ];

  const activeLanguage: AppLanguage = lang;

  return (
    <div className="app-shell">
      <ScrollToTop />

      <header className="header">
        <div className="container header-inner">
          <Logo />

          <nav
            className={`navigation ${menuOpen ? "open" : ""}`}
            aria-label="Main navigation"
          >
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                end={item.end}
                className={({ isActive }) =>
                  isActive ? "nav-link active" : "nav-link"
                }
                onClick={() => setMenuOpen(false)}
              >
                {item.label}
              </NavLink>
            ))}

            <Link
              className="mobile-login"
              to="/login"
              onClick={() => setMenuOpen(false)}
            >
              {copy.login}
            </Link>
          </nav>

          <div className="header-controls">
            <div
              className="language-control"
              role="group"
              aria-label={t("language")}
            >
              <Languages size={16} />

              <button
                type="button"
                className={
                  activeLanguage === "bn" ? "selected" : ""
                }
                aria-pressed={activeLanguage === "bn"}
                onClick={() => void changeAppLanguage("bn")}
              >
                বাংলা
              </button>

              <span className="language-separator">/</span>

              <button
                type="button"
                className={
                  activeLanguage === "en" ? "selected" : ""
                }
                aria-pressed={activeLanguage === "en"}
                onClick={() => void changeAppLanguage("en")}
              >
                EN
              </button>
            </div>

            <button
              type="button"
              className="theme-toggle"
              aria-label={copy.theme}
              title={
                theme === "light" ? copy.dark : copy.light
              }
              onClick={() =>
                setTheme((current) =>
                  current === "light" ? "dark" : "light"
                )
              }
            >
              {theme === "light" ? (
                <Moon size={19} />
              ) : (
                <Sun size={19} />
              )}
            </button>

            <Link to="/login" className="header-login">
              {copy.login}
              <ArrowUpRight size={16} />
            </Link>

            <button
              type="button"
              className="menu-toggle"
              aria-label={
                menuOpen ? copy.closeMenu : copy.openMenu
              }
              aria-expanded={menuOpen}
              onClick={() => setMenuOpen((open) => !open)}
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

      <main>{children}</main>

      <footer className="footer">
        <div className="container footer-main">
          <div className="footer-identity">
            <Logo />
            <p>{copy.footerDescription}</p>
          </div>

          <div className="footer-links">
            <h4>{copy.footerExplore}</h4>
            <Link to="/services">{t("navServices")}</Link>
            <Link to="/how-it-works">{t("navHow")}</Link>
            <Link to="/ai-assistant">{t("navAi")}</Link>
            <Link to="/about">
              {lang === "bn"
                ? "আমাদের সম্পর্কে"
                : "About us"}
            </Link>
          </div>

          <div className="footer-info">
            <h4>{copy.footerNotice}</h4>
            <p>{copy.disclaimer}</p>
            <span className="footer-demo">
              <ShieldCheck size={15} />
              {copy.demo}
            </span>
          </div>
        </div>

        <div className="container footer-bottom">
          <span>
            © {new Date().getFullYear()} JonoSeba.
          </span>
          <span>
            {lang === "bn"
              ? "নাগরিক সেবা সহজ করার প্রয়াস"
              : "Making citizen services simpler"}
          </span>
        </div>
      </footer>
    </div>
  );
}

/*
 * New homepage illustration.
 *
 * Decorative SVG: no external image or asset required.
 * The visual responds to the existing light/dark theme.
 */
function CityIllustration() {
  return (
    <div className="city-visual" aria-hidden="true">
      <div className="city-glow" />

      <div className="city-floating city-floating-top">
        <span className="city-float-icon">
          <Sparkles size={21} />
        </span>
        <div>
          <strong>JonoSeba</strong>
          <small>Digital Citizen Services</small>
        </div>
      </div>

      <svg
        className="city-artwork"
        viewBox="0 0 620 530"
        role="presentation"
        xmlns="http://www.w3.org/2000/svg"
      >
        <defs>
          <linearGradient
            id="skyGlow"
            x1="0"
            y1="0"
            x2="1"
            y2="1"
          >
            <stop offset="0%" stopColor="#b7f1de" />
            <stop offset="100%" stopColor="#d7ebff" />
          </linearGradient>

          <linearGradient
            id="civicBuilding"
            x1="0"
            y1="0"
            x2="1"
            y2="1"
          >
            <stop offset="0%" stopColor="#faffff" />
            <stop offset="100%" stopColor="#cfebe8" />
          </linearGradient>

          <linearGradient
            id="mainRoof"
            x1="0"
            y1="0"
            x2="1"
            y2="1"
          >
            <stop offset="0%" stopColor="#009c8c" />
            <stop offset="100%" stopColor="#05766f" />
          </linearGradient>

          <filter
            id="buildingShadow"
            x="-30%"
            y="-30%"
            width="160%"
            height="180%"
          >
            <feDropShadow
              dx="0"
              dy="18"
              stdDeviation="16"
              floodColor="#125c60"
              floodOpacity="0.13"
            />
          </filter>
        </defs>

        {/* Large background circle */}
        <circle
          cx="320"
          cy="255"
          r="209"
          fill="url(#skyGlow)"
          opacity=".58"
        />
        <circle
          cx="320"
          cy="255"
          r="237"
          stroke="#49b8ab"
          strokeOpacity=".17"
          strokeWidth="2"
          fill="none"
          strokeDasharray="7 13"
        />

        {/* Sun and clouds */}
        <circle cx="462" cy="95" r="30" fill="#ffd785" />

        <g fill="#ffffff" opacity=".88">
          <rect x="87" y="132" width="105" height="20" rx="10" />
          <circle cx="119" cy="132" r="20" />
          <circle cx="155" cy="128" r="25" />

          <rect x="418" y="158" width="113" height="18" rx="9" />
          <circle cx="449" cy="153" r="21" />
          <circle cx="484" cy="152" r="25" />
        </g>

        {/* Distant city */}
        <g opacity=".48">
          <rect
            x="92"
            y="248"
            width="76"
            height="142"
            rx="8"
            fill="#90c5c9"
          />
          <rect
            x="152"
            y="225"
            width="67"
            height="165"
            rx="8"
            fill="#acd3d7"
          />
          <rect
            x="428"
            y="227"
            width="77"
            height="165"
            rx="8"
            fill="#93c8ce"
          />
          <rect
            x="494"
            y="264"
            width="47"
            height="126"
            rx="8"
            fill="#b0d9da"
          />

          {[
            [109, 270],
            [134, 270],
            [109, 297],
            [134, 297],
            [109, 324],
            [134, 324],
            [170, 249],
            [193, 249],
            [170, 276],
            [193, 276],
            [449, 252],
            [474, 252],
            [449, 280],
            [474, 280],
          ].map(([x, y]) => (
            <rect
              key={`${x}-${y}`}
              x={x}
              y={y}
              width="12"
              height="17"
              rx="3"
              fill="#ffffff"
              opacity=".75"
            />
          ))}
        </g>

        {/* Ground and walkway */}
        <ellipse
          cx="310"
          cy="431"
          rx="259"
          ry="53"
          fill="#b9e1d8"
        />
        <ellipse
          cx="310"
          cy="448"
          rx="237"
          ry="31"
          fill="#d8f0e8"
        />
        <path
          d="M270 411 L348 411 L405 492 L218 492 Z"
          fill="#f4f7f1"
        />
        <path
          d="M280 425 L337 425 L355 454 L262 454 Z"
          fill="#d5e2dc"
        />

        {/* Main municipal building */}
        <g filter="url(#buildingShadow)">
          <rect
            x="201"
            y="213"
            width="222"
            height="210"
            rx="8"
            fill="url(#civicBuilding)"
            stroke="#83bdb7"
            strokeWidth="2"
          />

          <rect
            x="216"
            y="230"
            width="191"
            height="22"
            rx="4"
            fill="#c5e5df"
          />

          <path
            d="M175 208 L310 131 L450 208 L445 221 L180 221 Z"
            fill="url(#mainRoof)"
          />

          <path
            d="M310 149 L414 207 L207 207 Z"
            fill="#b4e5d9"
          />

          <path
            d="M185 221 H439 V238 H185 Z"
            fill="#06877c"
          />

          <circle
            cx="310"
            cy="186"
            r="17"
            fill="#ffffff"
            opacity=".96"
          />

          <path
            d="M301 190 V181 H319 V190 M298 193 H322"
            fill="none"
            stroke="#087d74"
            strokeWidth="3"
            strokeLinecap="round"
          />

          {/* Columns */}
          {[229, 276, 323, 370].map((x) => (
            <g key={x}>
              <rect
                x={x}
                y="259"
                width="26"
                height="128"
                rx="5"
                fill="#ffffff"
                stroke="#9acdc7"
                strokeWidth="1.5"
              />
              <rect
                x={x - 5}
                y="255"
                width="36"
                height="12"
                rx="3"
                fill="#ebfbf6"
              />
              <rect
                x={x - 5}
                y="382"
                width="36"
                height="13"
                rx="3"
                fill="#d2eae4"
              />
            </g>
          ))}

          {/* Door */}
          <path
            d="M292 423 V349 Q292 331 310 331 Q328 331 328 349 V423 Z"
            fill="#087e79"
          />
          <path
            d="M298 423 V352 Q298 337 310 337 Q322 337 322 352 V423"
            fill="none"
            stroke="#91d7c7"
            strokeWidth="3"
          />

          <circle cx="317" cy="387" r="3" fill="#d6f7ea" />

          <rect
            x="189"
            y="396"
            width="245"
            height="15"
            rx="4"
            fill="#94c9bf"
          />
          <rect
            x="178"
            y="411"
            width="268"
            height="14"
            rx="4"
            fill="#70b5aa"
          />
        </g>

        {/* Trees left */}
        <rect
          x="111"
          y="352"
          width="15"
          height="83"
          rx="6"
          fill="#9b795a"
        />
        <circle cx="119" cy="329" r="38" fill="#36b58c" />
        <circle cx="95" cy="350" r="29" fill="#5bd4a0" />
        <circle cx="143" cy="351" r="30" fill="#1b9f7f" />

        {/* Trees right */}
        <rect
          x="480"
          y="359"
          width="14"
          height="78"
          rx="6"
          fill="#9b795a"
        />
        <circle cx="486" cy="340" r="38" fill="#36b58c" />
        <circle cx="463" cy="356" r="28" fill="#5bd4a0" />
        <circle cx="508" cy="362" r="29" fill="#1b9f7f" />

        {/* Flower beds */}
        <g fill="#1fab82">
          <ellipse cx="159" cy="436" rx="28" ry="13" />
          <ellipse cx="457" cy="439" rx="30" ry="13" />
          <ellipse cx="101" cy="443" rx="23" ry="9" />
          <ellipse cx="521" cy="439" rx="24" ry="10" />
        </g>

        <g fill="#f4aa86">
          <circle cx="150" cy="427" r="5" />
          <circle cx="165" cy="434" r="4" />
          <circle cx="460" cy="428" r="5" />
          <circle cx="479" cy="435" r="4" />
        </g>

        {/* Decorative stars */}
        <g fill="#20b99d">
          <circle cx="105" cy="215" r="5" />
          <circle cx="511" cy="221" r="5" />
          <circle cx="420" cy="100" r="4" />
        </g>
      </svg>

      <div className="city-floating city-floating-bottom">
        <span className="city-float-icon city-float-blue">
          <ShieldCheck size={22} />
        </span>
        <div>
          <strong>Citizen First</strong>
          <small>Simple · Accessible · Digital</small>
        </div>
      </div>
    </div>
  );
}

function HomePage() {
  const { t } = useTranslation();
  const { copy } = useSiteLanguage();

  return (
    <section className="hero">
      <div className="container hero-layout">
        <div className="hero-copy">
          <div className="eyebrow">
            <span className="pulse-dot" />
            {copy.homeEyebrow}
          </div>

          <h1>
            <span>{copy.homeTitleOne}</span>
            <span className="hero-accent">
              {copy.homeTitleTwo}
            </span>
            <span>{copy.homeTitleThree}</span>
          </h1>

          <p className="hero-description">
            {copy.homeDescription}
          </p>

          <div className="hero-actions">
            <Link to="/services" className="btn btn-primary">
              {copy.explore}
              <ArrowRight size={19} />
            </Link>

            <Link
              to="/ai-assistant"
              className="btn btn-outline"
            >
              <Sparkles size={19} />
              {t("navAi")}
            </Link>
          </div>

          <div className="hero-trust">
            <ShieldCheck size={18} />
            <span>{copy.disclaimer}</span>
          </div>
        </div>

        <CityIllustration />
      </div>
    </section>
  );
}

function PageBanner({
  eyebrow,
  title,
  description,
}: {
  eyebrow: string;
  title: string;
  description?: string;
}) {
  return (
    <section className="page-banner">
      <div className="container">
        <span className="section-kicker">{eyebrow}</span>
        <h1>{title}</h1>
        {description && <p>{description}</p>}
      </div>
    </section>
  );
}

function ServiceCard({
  service,
}: {
  service: (typeof services)[number];
}) {
  const { lang } = useSiteLanguage();
  const Icon = serviceIcons[service.id];

  return (
    <Link
      to={`/services/${service.id}`}
      className={`service-card service-${service.id}`}
    >
      <div className="service-card-top">
        <span className="service-icon">
          <Icon size={26} strokeWidth={1.8} />
        </span>
        <ArrowUpRight className="service-arrow" size={21} />
      </div>

      <h3>{service.title[lang]}</h3>
      <p>{service.description[lang]}</p>

      <span className="service-card-action">
        {lang === "bn"
          ? "বিস্তারিত দেখুন"
          : "Explore service"}
        <ArrowRight size={17} />
      </span>
    </Link>
  );
}

function ServicesPage() {
  const { copy } = useSiteLanguage();

  return (
    <>
      <PageBanner
        eyebrow="JONOSEBA SERVICES"
        title={copy.servicesTitle}
        description={copy.servicesIntro}
      />

      <section className="section inner-section">
        <div className="container services-grid">
          {services.map((service) => (
            <ServiceCard
              key={service.id}
              service={service}
            />
          ))}
        </div>
      </section>
    </>
  );
}

function NotFoundPage() {
  const { copy } = useSiteLanguage();

  return (
    <section className="not-found">
      <div className="container">
        <span className="not-found-number">404</span>
        <h1>{copy.notFound}</h1>
        <Link to="/" className="btn btn-primary">
          {copy.backHome}
          <ArrowRight size={18} />
        </Link>
      </div>
    </section>
  );
}

function ServiceDetailsPage() {
  const { id } = useParams();
  const { lang, copy } = useSiteLanguage();

  const service = services.find(
    (entry) => entry.id === id
  );

  if (!service) {
    return <NotFoundPage />;
  }

  const Icon = serviceIcons[service.id];

  return (
    <>
      <PageBanner
        eyebrow="MUNICIPAL SERVICE GUIDE"
        title={service.title[lang]}
        description={service.description[lang]}
      />

      <section className="section inner-section">
        <div className="container detail-layout">
          <div className="detail-main">
            <div className="detail-title">
              <span className="detail-icon">
                <Icon size={28} />
              </span>
              <h2>{copy.serviceDetailTitle}</h2>
            </div>

            <div className="detail-block">
              <h3>{copy.serviceDocuments}</h3>
              <p>{service.preparation[lang]}</p>
            </div>

            <div className="detail-block">
              <h3>{copy.serviceProcess}</h3>
              <p>{service.process[lang]}</p>
            </div>

            <div className="detail-block">
              <h3>{copy.serviceFees}</h3>
              <p>{copy.serviceFeeNote}</p>
            </div>

            <Link to="/services" className="btn btn-outline">
              <ArrowRight size={18} />
              {copy.backServices}
            </Link>
          </div>

          <aside className="detail-aside">
            <ShieldCheck size={29} />
            <h3>{copy.demo}</h3>
            <p>{copy.serviceDetailNote}</p>
          </aside>
        </div>
      </section>
    </>
  );
}

function HowPage() {
  const { copy } = useSiteLanguage();

  const steps = [
    {
      number: "01",
      icon: Search,
      title: copy.howOne,
      text: copy.howOneText,
    },
    {
      number: "02",
      icon: Sparkles,
      title: copy.howTwo,
      text: copy.howTwoText,
    },
    {
      number: "03",
      icon: MessageCircle,
      title: copy.howThree,
      text: copy.howThreeText,
    },
  ];

  return (
    <>
      <PageBanner
        eyebrow="HOW IT WORKS"
        title={copy.howTitle}
        description={copy.howIntro}
      />

      <section className="section inner-section">
        <div className="container steps-grid">
          {steps.map((step) => {
            const Icon = step.icon;

            return (
              <article
                className="step-card"
                key={step.number}
              >
                <span className="step-number">
                  {step.number}
                </span>

                <span className="step-icon">
                  <Icon size={26} />
                </span>

                <h3>{step.title}</h3>
                <p>{step.text}</p>
              </article>
            );
          })}
        </div>
      </section>
    </>
  );
}

function AiPage() {
  const { copy } = useSiteLanguage();

  return (
    <>
      <PageBanner
        eyebrow="JONOSEBA AI"
        title={copy.aiTitle}
        description={copy.aiIntro}
      />

      <section className="section inner-section">
        <div className="container ai-page-layout">
          <div className="ai-page-copy">
            <span className="ai-page-icon">
              <Sparkles size={30} />
            </span>
            <h2>{copy.aiComing}</h2>
            <p>{copy.disclaimer}</p>

            <Link
              to="/login"
              className="btn btn-primary"
            >
              <LockKeyhole size={18} />
              {copy.login}
            </Link>
          </div>

          <div className="chat-preview">
            <div className="chat-preview-header">
              <span className="chat-avatar">
                <Sparkles size={22} />
              </span>
              <div>
                <strong>JonoSeba AI</strong>
                <small>{copy.demo}</small>
              </div>
            </div>

            <div className="chat-preview-question">
              {copy.aiQuestion}
            </div>

            <div className="chat-preview-note">
              <ShieldCheck size={17} />
              {copy.aiAnswer}
            </div>
          </div>
        </div>
      </section>
    </>
  );
}

function AboutPage() {
  const { copy } = useSiteLanguage();

  return (
    <>
      <PageBanner
        eyebrow="ABOUT THE PROJECT"
        title={copy.aboutTitle}
        description={copy.aboutText}
      />

      <section className="section inner-section">
        <div className="container about-panel">
          <span className="about-icon">
            <Landmark size={34} />
          </span>

          <h2>JonoSeba · জনসেবা</h2>
          <p>{copy.footerDescription}</p>
          <p>{copy.disclaimer}</p>

          <Link
            to="/services"
            className="btn btn-primary"
          >
            {copy.explore}
            <ArrowRight size={18} />
          </Link>
        </div>
      </section>
    </>
  );
}

function AuthPreviewPage({
  mode,
}: {
  mode: "login" | "register";
}) {
  const { copy } = useSiteLanguage();
  const isLogin = mode === "login";

  return (
    <section className="auth-page">
      <div className="auth-card">
        <span className="auth-icon">
          <LockKeyhole size={28} />
        </span>

        <span className="section-kicker">
          JONOSEBA ACCOUNT
        </span>

        <h1>
          {isLogin
            ? copy.loginTitle
            : copy.registerTitle}
        </h1>

        <p>
          {isLogin
            ? copy.loginText
            : copy.registerText}
        </p>

        <div className="auth-notice">
          <ShieldCheck size={19} />
          <span>{copy.demo}</span>
        </div>

        <div className="auth-page-links">
          <Link
            to={isLogin ? "/register" : "/login"}
            className="btn btn-outline"
          >
            {isLogin ? copy.register : copy.login}
          </Link>

          <Link to="/" className="text-action">
            {copy.backHome}
            <ArrowRight size={17} />
          </Link>
        </div>
      </div>
    </section>
  );
}

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route
          path="/services"
          element={<ServicesPage />}
        />
        <Route
          path="/services/:id"
          element={<ServiceDetailsPage />}
        />
        <Route
          path="/how-it-works"
          element={<HowPage />}
        />
        <Route
          path="/ai-assistant"
          element={<AiPage />}
        />
        <Route
          path="/about"
          element={<AboutPage />}
        />
        <Route
          path="/login"
          element={<AuthPreviewPage mode="login" />}
        />
        <Route
          path="/register"
          element={<AuthPreviewPage mode="register" />}
        />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Layout>
  );
}

export default App;
