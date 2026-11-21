import i18n from "i18next";
import { initReactI18next } from "react-i18next";

export type AppLanguage = "bn" | "en";

const STORAGE_KEY = "jonoseba-language";

function initialLanguage(): AppLanguage {
  try {
    return localStorage.getItem(STORAGE_KEY) === "en"
      ? "en"
      : "bn";
  } catch {
    return "bn";
  }
}

export async function changeAppLanguage(
  language: AppLanguage,
): Promise<void> {
  await i18n.changeLanguage(language);
  document.documentElement.lang = language;

  try {
    localStorage.setItem(STORAGE_KEY, language);
  } catch {
    // Language switching still works without storage.
  }
}

const resources = {
  bn: {
    translation: {
      brand: "জনসেবা",
      brandTag: "নাগরিক সেবা প্ল্যাটফর্ম",
      navHome: "হোম",
      navServices: "সেবাসমূহ",
      navHow: "যেভাবে কাজ করে",
      navAi: "AI সহকারী",
      demo: "শিক্ষামূলক ডেমো",
      heroLabel: "আপনার শহর • আপনার সেবা",
      heroTitle: "নাগরিক সেবা, এখন আরও সহজ",
      heroDescription:
        "পৌরসভার প্রয়োজনীয় সেবার তথ্য, নাগরিক সমস্যার সমাধানের পথ এবং AI-ভিত্তিক সহায়তা—সবকিছু একটি প্ল্যাটফর্মে।",
      explore: "সেবাসমূহ দেখুন",
      discoverAi: "AI সহকারী সম্পর্কে জানুন",
      disclaimer:
        "এটি একটি শিক্ষামূলক ডেমো প্রজেক্ট; সরকারি কর্তৃপক্ষের অনুমোদিত পোর্টাল নয়।",
      servicesLabel: "পৌর নাগরিক সেবা",
      servicesTitle: "আপনার প্রয়োজনীয় সেবা খুঁজুন",
      servicesDescription:
        "পৌরসভার গুরুত্বপূর্ণ সেবাগুলো এক জায়গায় জানুন। বিস্তারিত অনলাইন সুবিধা পর্যায়ক্রমে যুক্ত হবে।",
      birth: "জন্ম ও মৃত্যু নিবন্ধন",
      birthDesc:
        "নতুন নিবন্ধন, তথ্য সংশোধন এবং সনদ পুনঃমুদ্রণ।",
      trade: "ট্রেড লাইসেন্স",
      tradeDesc:
        "নতুন ব্যবসার লাইসেন্স ও নবায়ন সম্পর্কিত তথ্য।",
      certificate: "নাগরিক ও ওয়ারিশ সনদ",
      certificateDesc:
        "নাগরিকত্ব, চারিত্রিক ও ওয়ারিশ সনদের নির্দেশনা।",
      tax: "হোল্ডিং ট্যাক্স",
      taxDesc:
        "হোল্ডিং নম্বর, কর এবং মালিকানা পরিবর্তনের তথ্য।",
      water: "পানি ও অবকাঠামো",
      waterDesc:
        "পানির সংযোগ, রাস্তা, ড্রেন ও অবকাঠামো সেবা।",
      health: "স্বাস্থ্য ও পরিবেশ",
      healthDesc:
        "টিকাদান, মশক নিয়ন্ত্রণ ও স্বাস্থ্যসেবা।",
      comingSoon: "বিস্তারিত সুবিধা শিগগিরই",
      howLabel: "সহজ প্রক্রিয়া",
      howTitle: "জনসেবা যেভাবে সাহায্য করবে",
      stepOne: "সেবা নির্বাচন করুন",
      stepOneDesc: "আপনার প্রয়োজন অনুযায়ী সেবার ধরন খুঁজুন।",
      stepTwo: "AI নির্দেশনা নিন",
      stepTwoDesc:
        "প্রকাশিত তথ্যের ভিত্তিতে প্রশ্নের উত্তর পাওয়ার সুবিধা আসছে।",
      stepThree: "অভিযোগ ব্যবস্থাপনা",
      stepThreeDesc:
        "নাগরিক অভিযোগ জমা ও অগ্রগতি দেখার সুবিধা যুক্ত হবে।",
      aiLabel: "JonoSeba AI",
      aiTitle: "নাগরিক প্রশ্নের জন্য AI সহকারী",
      aiDescription:
        "আমাদের AI backend প্রস্তুত। এই ওয়েবসাইট থেকে সরাসরি চ্যাট করার সুবিধা পরের ধাপে যুক্ত হবে।",
      aiExample: "জন্মনিবন্ধনের জন্য কী কী কাগজ লাগে?",
      aiPending: "চ্যাট ইন্টারফেস শিগগিরই আসছে",
      footer:
        "বাংলাদেশের পৌর নাগরিক সেবা সহজ করার একটি শিক্ষামূলক উদ্যোগ।",
      language: "ভাষা",
      mobileMenu: "মেনু",
    },
  },
  en: {
    translation: {
      brand: "JonoSeba",
      brandTag: "Citizen Service Platform",
      navHome: "Home",
      navServices: "Services",
      navHow: "How it works",
      navAi: "AI Assistant",
      demo: "Educational Demo",
      heroLabel: "Your City • Your Services",
      heroTitle: "Citizen services, made simpler",
      heroDescription:
        "Explore municipal services, find guidance for civic issues, and discover AI-powered assistance in one place.",
      explore: "Explore Services",
      discoverAi: "Meet the AI Assistant",
      disclaimer:
        "This is an educational demo project, not a government-authorized portal.",
      servicesLabel: "Municipal Services",
      servicesTitle: "Find the service you need",
      servicesDescription:
        "Explore essential municipal services. Detailed online features will be connected in upcoming steps.",
      birth: "Birth & Death Registration",
      birthDesc:
        "New registration, corrections, and certificate reprints.",
      trade: "Trade License",
      tradeDesc:
        "Information on new licenses and renewals.",
      certificate: "Citizen & Heir Certificates",
      certificateDesc:
        "Guidance on citizenship, character, and heir certificates.",
      tax: "Holding Tax",
      taxDesc:
        "Holding numbers, assessments, and ownership changes.",
      water: "Water & Infrastructure",
      waterDesc:
        "Water connections, roads, drains, and infrastructure.",
      health: "Health & Environment",
      healthDesc:
        "Immunization, mosquito control, and health services.",
      comingSoon: "Details coming soon",
      howLabel: "Simple Process",
      howTitle: "How JonoSeba will help",
      stepOne: "Choose a service",
      stepOneDesc: "Find the service that matches your needs.",
      stepTwo: "Get AI guidance",
      stepTwoDesc:
        "Ask questions using published knowledge in a future step.",
      stepThree: "Manage complaints",
      stepThreeDesc:
        "Complaint submission and tracking will be connected.",
      aiLabel: "JonoSeba AI",
      aiTitle: "An AI assistant for citizen questions",
      aiDescription:
        "Our AI backend is ready. Direct chat from this website will be connected in an upcoming step.",
      aiExample:
        "What documents do I need for birth registration?",
      aiPending: "Chat interface coming soon",
      footer:
        "An educational initiative for accessible municipal services in Bangladesh.",
      language: "Language",
      mobileMenu: "Menu",
    },
  },
} as const;

void i18n.use(initReactI18next).init({
  resources,
  lng: initialLanguage(),
  fallbackLng: "bn",
  supportedLngs: ["bn", "en"],
  interpolation: {
    escapeValue: false,
  },
  react: {
    useSuspense: false,
  },
});

export default i18n;
