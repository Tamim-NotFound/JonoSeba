
export type SiteLanguage = "bn" | "en";
export type ServiceId =
  | "birth"
  | "trade"
  | "certificate"
  | "tax"
  | "water"
  | "health";

export const siteCopy = {
  bn: {
    homeEyebrow: "বাংলাদেশের নাগরিক সেবার নতুন অভিজ্ঞতা",
    homeTitleOne: "আপনার শহর।",
    homeTitleTwo: "আপনার সেবা।",
    homeTitleThree: "আপনার হাতেই।",
    homeDescription:
      "পৌরসেবার তথ্য খোঁজা থেকে নাগরিক সমস্যার সঠিক পথ জানা—জনসেবা তৈরি হচ্ছে একটি সহজ, আধুনিক ও বাংলা-প্রথম অভিজ্ঞতা নিয়ে।",
    explore: "সেবাসমূহ ঘুরে দেখুন",
    learnMore: "বিস্তারিত জানুন",
    heroCardTitle: "আপনার ডিজিটাল সেবা কেন্দ্র",
    heroCardSubtitle: "JonoSeba Citizen Portal",
    heroCardOne: "প্রয়োজনীয় সেবার তথ্য",
    heroCardTwo: "AI-ভিত্তিক সহায়তা",
    heroCardThree: "অভিযোগ ব্যবস্থাপনা",
    heroCardNote: "সেবা ও ফিচার পর্যায়ক্রমে যুক্ত হচ্ছে",
    featureLabel: "কেন জনসেবা?",
    featureTitle: "নাগরিকদের কথা ভেবেই ডিজাইন",
    featureOne: "বাংলা ও ইংরেজি",
    featureOneText: "নিজের পছন্দের ভাষায় সহজে তথ্য জানুন।",
    featureTwo: "মোবাইল-ফ্রেন্ডলি",
    featureTwoText: "ফোন, ট্যাবলেট বা কম্পিউটার—সবখানে ব্যবহারযোগ্য।",
    featureThree: "সহজ নেভিগেশন",
    featureThreeText: "দরকারি সেবা খুঁজতে অপ্রয়োজনীয় জটিলতা নেই।",
    servicesTitle: "পৌর নাগরিক সেবাসমূহ",
    servicesIntro:
      "সেবা বেছে নিয়ে তার আলাদা পেজে যান। বর্তমানে তথ্যগুলো গবেষণা ও পর্যালোচনার পর্যায়ে আছে।",
    featuredTitle: "জনপ্রিয় সেবাগুলো দেখে নিন",
    serviceDetailTitle: "সেবার প্রাথমিক তথ্য",
    serviceDetailNote:
      "এই তথ্য গবেষণাভিত্তিক। নির্দিষ্ট কাগজপত্র, ফি ও নিয়ম সংশ্লিষ্ট কর্তৃপক্ষের কাছ থেকে নিশ্চিত করুন।",
    serviceProcess: "কীভাবে শুরু করবেন",
    serviceDocuments: "প্রস্তুতির বিষয়",
    serviceFees: "ফি সম্পর্কে",
    serviceFeeNote:
      "ফি স্থান, সেবার ধরন ও বর্তমান তফসিল অনুযায়ী আলাদা হতে পারে। যাচাইকৃত ফি এখানে পরবর্তীতে দেখানো হবে।",
    backServices: "সব সেবা দেখুন",
    howTitle: "জনসেবা যেভাবে কাজ করবে",
    howIntro:
      "একটি সহজ ডিজিটাল অভিজ্ঞতা তৈরির কাজ চলছে।",
    howOne: "সেবা খুঁজুন",
    howOneText: "আপনার প্রয়োজন অনুযায়ী সেবা নির্বাচন করুন।",
    howTwo: "নির্দেশনা নিন",
    howTwoText: "প্রকাশিত তথ্যভান্ডার থেকে AI সহায়তা নিন।",
    howThree: "অভিযোগ জানান",
    howThreeText: "লগইন করে অভিযোগ জমা ও অগ্রগতি অনুসরণ করুন।",
    aiTitle: "আপনার পাশে JonoSeba AI",
    aiIntro:
      "আমাদের AI backend রয়েছে। লগইন ও চ্যাটের frontend সংযোগ পরবর্তী ধাপে যুক্ত হবে।",
    aiQuestion: "“জন্মনিবন্ধন সংশোধন করতে কী লাগে?”",
    aiAnswer:
      "এটি শুধু ডিজাইন প্রিভিউ। এখানে এখনো AI-এর বাস্তব উত্তর দেখানো হচ্ছে না।",
    aiComing: "লাইভ চ্যাট সংযোগের কাজ বাকি",
    aboutTitle: "জনসেবা সম্পর্কে",
    aboutText:
      "JonoSeba বাংলাদেশের পৌর নাগরিক সেবার তথ্য ও অভিযোগ ব্যবস্থাপনাকে সহজ করার লক্ষ্যে তৈরি একটি শিক্ষামূলক সফটওয়্যার প্রকল্প। এটি কোনো সরকারি পোর্টাল নয়।",
    loginTitle: "আপনার অ্যাকাউন্টে লগইন",
    loginText:
      "নিরাপদ লগইন ফর্মটি বিদ্যমান FastAPI authentication-এর সঙ্গে পরের ধাপে যুক্ত হবে। এখানে এখনো লগইন করা যাচ্ছে না।",
    registerTitle: "নতুন অ্যাকাউন্ট",
    registerText:
      "নাগরিক নিবন্ধন ব্যবস্থা backend-এর সঙ্গে যুক্ত করার কাজ পরবর্তী ধাপে হবে।",
    login: "লগইন",
    register: "নিবন্ধন",
    theme: "রঙের ধরন পরিবর্তন",
    light: "লাইট মোড",
    dark: "ডার্ক মোড",
    openMenu: "মেনু খুলুন",
    closeMenu: "মেনু বন্ধ করুন",
    demo: "শিক্ষামূলক ডেমো",
    disclaimer:
      "এটি শিক্ষামূলক ডেমো, সরকারি কর্তৃপক্ষের অনুমোদিত পোর্টাল নয়।",
    notFound: "এই পেজটি পাওয়া যায়নি",
    backHome: "হোমে ফিরে যান",
    footerDescription:
      "নাগরিক সেবা সহজ, স্বচ্ছ ও সবার জন্য ব্যবহারযোগ্য করার একটি উদ্যোগ।",
    footerExplore: "এক্সপ্লোর করুন",
    footerNotice: "গুরুত্বপূর্ণ তথ্য",
  },
  en: {
    homeEyebrow: "A better citizen-service experience for Bangladesh",
    homeTitleOne: "Your city.",
    homeTitleTwo: "Your services.",
    homeTitleThree: "In your hands.",
    homeDescription:
      "From finding municipal service information to understanding civic issues, JonoSeba is being built as a simple, modern, accessible experience.",
    explore: "Explore Services",
    learnMore: "Learn More",
    heroCardTitle: "Your digital service center",
    heroCardSubtitle: "JonoSeba Citizen Portal",
    heroCardOne: "Municipal information",
    heroCardTwo: "AI-powered guidance",
    heroCardThree: "Complaint management",
    heroCardNote: "Features are being introduced step by step",
    featureLabel: "Why JonoSeba?",
    featureTitle: "Designed around citizens",
    featureOne: "Bengali and English",
    featureOneText: "Find information in your preferred language.",
    featureTwo: "Mobile-friendly",
    featureTwoText: "Built for phones, tablets, and computers.",
    featureThree: "Simple navigation",
    featureThreeText: "Reach the right service without unnecessary complexity.",
    servicesTitle: "Municipal Citizen Services",
    servicesIntro:
      "Select a service to visit its dedicated page. The guidance is still undergoing research and review.",
    featuredTitle: "Explore essential services",
    serviceDetailTitle: "Initial service information",
    serviceDetailNote:
      "This is research-based guidance. Confirm exact requirements, documents, and fees with the responsible authority.",
    serviceProcess: "How to get started",
    serviceDocuments: "What to prepare",
    serviceFees: "Fees",
    serviceFeeNote:
      "Fees depend on the service, location, and current schedule. Verified amounts will be published here later.",
    backServices: "Browse all services",
    howTitle: "How JonoSeba will work",
    howIntro:
      "We are building a simpler digital experience.",
    howOne: "Find a service",
    howOneText: "Select the service that matches your needs.",
    howTwo: "Get guidance",
    howTwoText: "Access AI guidance using published knowledge.",
    howThree: "Report an issue",
    howThreeText: "Sign in to submit and track civic complaints.",
    aiTitle: "Meet JonoSeba AI",
    aiIntro:
      "Our AI backend exists. Secure login and the frontend chat connection will be added in the next stages.",
    aiQuestion: '"How can I correct a birth certificate?"',
    aiAnswer:
      "This is a visual preview only. No real AI answer is being generated here yet.",
    aiComing: "Live chat integration pending",
    aboutTitle: "About JonoSeba",
    aboutText:
      "JonoSeba is an educational software project designed to make municipal service information and civic complaint management more accessible in Bangladesh. It is not an official government portal.",
    loginTitle: "Sign in to your account",
    loginText:
      "The secure sign-in form will be connected to the existing FastAPI authentication system in the next step. Sign-in is not available here yet.",
    registerTitle: "Create an account",
    registerText:
      "Citizen registration will be connected to the backend in the next step.",
    login: "Sign In",
    register: "Register",
    theme: "Change color theme",
    light: "Light Mode",
    dark: "Dark Mode",
    openMenu: "Open menu",
    closeMenu: "Close menu",
    demo: "Educational Demo",
    disclaimer:
      "An educational demo, not a government-authorized portal.",
    notFound: "Page not found",
    backHome: "Return Home",
    footerDescription:
      "Making municipal services simpler, clearer, and more accessible.",
    footerExplore: "Explore",
    footerNotice: "Important notice",
  },
} as const;

export type SiteCopy = typeof siteCopy.bn;

type LocalizedText = {
  bn: string;
  en: string;
};

export type ServiceInfo = {
  id: ServiceId;
  title: LocalizedText;
  description: LocalizedText;
  preparation: LocalizedText;
  process: LocalizedText;
};

export const services: ServiceInfo[] = [
  {
    id: "birth",
    title: {
      bn: "জন্ম ও মৃত্যু নিবন্ধন",
      en: "Birth & Death Registration",
    },
    description: {
      bn: "নতুন নিবন্ধন, তথ্য সংশোধন, সনদ পুনঃমুদ্রণ এবং মৃত্যু নিবন্ধন।",
      en: "New registrations, corrections, reprints, and death registration.",
    },
    preparation: {
      bn: "নিবন্ধনের ধরন অনুযায়ী পরিচয় ও জন্ম/মৃত্যুর প্রমাণ প্রস্তুত রাখুন।",
      en: "Prepare identity and birth/death evidence relevant to your request.",
    },
    process: {
      bn: "বিদ্যমান রেকর্ড আছে কি না নিশ্চিত করুন; এরপর সংশ্লিষ্ট নিবন্ধক কার্যালয়ের বর্তমান নির্দেশনা অনুসরণ করুন।",
      en: "Check whether a record already exists, then follow the current instructions of the relevant registrar.",
    },
  },
  {
    id: "trade",
    title: {
      bn: "ট্রেড লাইসেন্স",
      en: "Trade License",
    },
    description: {
      bn: "নতুন ব্যবসার লাইসেন্স, নবায়ন ও ব্যবসার ধরন অনুযায়ী নির্দেশনা।",
      en: "New licenses, renewals, and business-specific guidance.",
    },
    preparation: {
      bn: "মালিকের পরিচয়, ব্যবসার ঠিকানা ও প্রযোজ্য ব্যবসায়িক কাগজপত্র প্রস্তুত করুন।",
      en: "Prepare owner identity, business address, and applicable business documents.",
    },
    process: {
      bn: "ব্যবসার ধরন নির্ধারণ করে স্থানীয় লাইসেন্স শাখার বর্তমান checklist যাচাই করুন।",
      en: "Identify your business type and review the local licensing office's current checklist.",
    },
  },
  {
    id: "certificate",
    title: {
      bn: "নাগরিক ও ওয়ারিশ সনদ",
      en: "Citizen & Heir Certificates",
    },
    description: {
      bn: "নাগরিকত্ব, চারিত্রিক ও ওয়ারিশ সনদ সম্পর্কিত সহায়তা।",
      en: "Guidance for citizenship, character, and heir certificates.",
    },
    preparation: {
      bn: "পরিচয়, ঠিকানা এবং ওয়ারিশ সনদের ক্ষেত্রে সম্পর্কের প্রমাণ প্রস্তুত করুন।",
      en: "Prepare identity, address, and relationship evidence when relevant.",
    },
    process: {
      bn: "সনদের ধরন বেছে সংশ্লিষ্ট ওয়ার্ড বা প্রশাসন শাখার প্রক্রিয়া যাচাই করুন।",
      en: "Select the certificate type and verify the ward or administrative office process.",
    },
  },
  {
    id: "tax",
    title: {
      bn: "হোল্ডিং ট্যাক্স",
      en: "Holding Tax",
    },
    description: {
      bn: "হোল্ডিং নম্বর, কর, মূল্যায়ন এবং মালিকানা পরিবর্তন।",
      en: "Holding numbers, taxes, assessments, and ownership changes.",
    },
    preparation: {
      bn: "হোল্ডিং তথ্য, মালিকানার দলিল ও পুরোনো কর রশিদ প্রযোজ্য ক্ষেত্রে রাখুন।",
      en: "Prepare holding details, ownership documents, and previous tax receipts if applicable.",
    },
    process: {
      bn: "নতুন হোল্ডিং, নাম পরিবর্তন বা কর পরিশোধ—কোন সেবা প্রয়োজন তা নির্ধারণ করুন।",
      en: "Determine whether you need a new holding, ownership update, or tax payment.",
    },
  },
  {
    id: "water",
    title: {
      bn: "পানি ও অবকাঠামো",
      en: "Water & Infrastructure",
    },
    description: {
      bn: "পানির সংযোগ, রাস্তা, ড্রেন ও স্থানীয় অবকাঠামো।",
      en: "Water connections, roads, drains, and local infrastructure.",
    },
    preparation: {
      bn: "সেবার ঠিকানা, হোল্ডিং তথ্য এবং সমস্যার বিস্তারিত প্রস্তুত রাখুন।",
      en: "Prepare the service address, holding information, and relevant issue details.",
    },
    process: {
      bn: "এলাকার দায়িত্বপ্রাপ্ত পৌরসভা বা সেবাদাতা কর্তৃপক্ষ নিশ্চিত করুন।",
      en: "Identify the municipality or service provider responsible for the area.",
    },
  },
  {
    id: "health",
    title: {
      bn: "স্বাস্থ্য ও পরিবেশ",
      en: "Health & Environment",
    },
    description: {
      bn: "EPI, মশক নিয়ন্ত্রণ ও পরিবেশ-সংক্রান্ত পৌরসেবা।",
      en: "EPI, mosquito control, and environment-related municipal services.",
    },
    preparation: {
      bn: "সেবার ধরন অনুযায়ী শিশুর তথ্য বা সমস্যার অবস্থান প্রস্তুত রাখুন।",
      en: "Prepare child details or the issue location, depending on the service.",
    },
    process: {
      bn: "স্থানীয় স্বাস্থ্য বিভাগ, EPI কেন্দ্র বা সংশ্লিষ্ট শাখার বর্তমান তথ্য যাচাই করুন।",
      en: "Verify current information with the local health office, EPI center, or relevant department.",
    },
  },
];
