from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DEFAULT_OUTPUT_PATH = (
    PROJECT_ROOT
    / "docs"
    / "knowledge"
    / "master_service_drafts.md"
)


@dataclass(frozen=True)
class MunicipalServiceGuide:
    """
    Research-derived municipal service guidance.

    These guides are not approved or published RAG
    knowledge. They require source review before use
    as confirmed government guidance.
    """

    key: str
    title_bn: str
    department_bn: str
    documents: tuple[str, ...]
    fees: tuple[str, ...]
    process: tuple[str, ...]
    notes: tuple[str, ...] = ()
    source_status: str = "research_pending"


SERVICE_GUIDES: tuple[MunicipalServiceGuide, ...] = (
    MunicipalServiceGuide(
        key="birth_registration_new",
        title_bn="নতুন জন্মনিবন্ধন",
        department_bn="জন্ম ও মৃত্যু নিবন্ধন শাখা",
        documents=(
            "০–৪৫ দিন: EPI/টিকাদান কার্ড, হাসপাতালের "
            "ছাড়পত্র বা জন্মসংক্রান্ত চিকিৎসা নথি "
            "(প্রযোজ্য ক্ষেত্রে)।",
            "৪৬ দিন–৫ বছর: জন্মের প্রমাণ, EPI কার্ড, "
            "অভিভাবকের পরিচয় এবং প্রযোজ্য ক্ষেত্রে "
            "স্কুলের প্রত্যয়নপত্র।",
            "৫ বছরের বেশি: শিক্ষাগত সনদ, "
            "প্রতিষ্ঠানপ্রধানের প্রত্যয়নপত্র অথবা "
            "গ্রহণযোগ্য বয়স-প্রমাণের দলিল।",
            "পিতা-মাতার NID এবং/অথবা অনলাইন "
            "জন্মনিবন্ধন তথ্য প্রযোজ্য নিয়ম অনুযায়ী।",
            "ঠিকানার প্রমাণ; হোল্ডিং ট্যাক্স রশিদ "
            "সর্বজনীন বাধ্যতামূলক কি না যাচাই প্রয়োজন।",
            "পিতা বা মাতা মৃত হলে প্রয়োজনীয় "
            "সহায়ক রেকর্ড সম্পর্কে নিবন্ধকের "
            "নির্দেশনা যাচাই করতে হবে।",
        ),
        fees=(
            "গবেষণায় উল্লিখিত: ৪৫ দিন পর্যন্ত "
            "বিনামূল্যে।",
            "গবেষণায় উল্লিখিত: ৪৬ দিন থেকে "
            "৫ বছর পর্যন্ত ২৫ টাকা।",
            "গবেষণায় উল্লিখিত: ৫ বছরের বেশি "
            "বয়সে ৫০ টাকা।",
            "এই অঙ্কগুলো বর্তমান সরকারি "
            "ফি তফসিল দিয়ে যাচাই করতে হবে।",
        ),
        process=(
            "আবেদনকারীর বয়স, জন্মস্থান এবং "
            "নিবন্ধন এলাকার ভিত্তিতে প্রয়োজনীয় "
            "দলিলের তালিকা যাচাই করুন।",
            "অনলাইন আবেদন ও নিবন্ধক কার্যালয়ে "
            "দলিল জমার বর্তমান নির্দেশনা অনুসরণ করুন।",
        ),
        notes=(
            "২০০১ সালের ১ জানুয়ারি-সংক্রান্ত "
            "পিতা-মাতার জন্মনিবন্ধন বাধ্যবাধকতার "
            "দাবি আলাদাভাবে যাচাই প্রয়োজন।",
            "অভিভাবকের জন্মনিবন্ধন নম্বর না থাকলে "
            "গ্রহণযোগ্য বিকল্প সম্পর্কে সংশ্লিষ্ট "
            "নিবন্ধক কার্যালয়ে জানতে হবে।",
        ),
    ),
    MunicipalServiceGuide(
        key="birth_registration_correction",
        title_bn="জন্মনিবন্ধনের তথ্য সংশোধন",
        department_bn="জন্ম ও মৃত্যু নিবন্ধন শাখা",
        documents=(
            "নাম বা বানান: শিক্ষা সনদ, NID, পাসপোর্ট "
            "অথবা শিশুর ক্ষেত্রে EPI/হাসপাতালের "
            "প্রমাণ প্রাসঙ্গিক হতে পারে।",
            "জন্মতারিখ: শিক্ষা সনদ, হাসপাতালের "
            "জন্মসংক্রান্ত দলিল, EPI কার্ড "
            "বা গ্রহণযোগ্য চিকিৎসা প্রমাণ।",
            "পিতা-মাতার নাম: তাঁদের পরিচয়পত্র, "
            "জন্মনিবন্ধন এবং সম্পর্কের দলিল।",
            "ঠিকানা: গ্রহণযোগ্য বসবাসের বা "
            "ঠিকানার প্রমাণ।",
        ),
        fees=(
            "গবেষণায় উল্লিখিত: জন্মতারিখ "
            "সংশোধনে ১০০ টাকা।",
            "গবেষণায় উল্লিখিত: অন্যান্য তথ্য "
            "সংশোধনে ৫০ টাকা।",
            "বর্তমান সরকারি তফসিল দিয়ে "
            "অঙ্কগুলো যাচাই করা বাকি।",
        ),
        process=(
            "বিদ্যমান জন্মনিবন্ধনের তথ্য "
            "শনাক্ত করুন।",
            "কোন তথ্য সংশোধন প্রয়োজন, সেই "
            "অনুযায়ী supporting documents প্রস্তুত করুন।",
            "বর্তমান BDRIS ও নিবন্ধক "
            "কার্যালয়ের সংশোধন প্রক্রিয়া যাচাই করুন।",
        ),
        notes=(
            "সর্বোচ্চ তিনবার সংশোধনের দাবিটি "
            "সরকারি বিধি দিয়ে যাচাই না করে "
            "নিশ্চিত নিয়ম বলা যাবে না।",
        ),
    ),
    MunicipalServiceGuide(
        key="birth_certificate_reprint",
        title_bn="হারানো জন্মসনদ পুনঃমুদ্রণ",
        department_bn="জন্ম ও মৃত্যু নিবন্ধন শাখা",
        documents=(
            "বিদ্যমান ১৭ ডিজিটের নিবন্ধন নম্বর "
            "অথবা পুরোনো সনদের কপি (যদি থাকে)।",
            "আবেদনকারীর পরিচয়পত্র; শিশুর ক্ষেত্রে "
            "অভিভাবকের পরিচয় সংক্রান্ত তথ্য।",
        ),
        fees=(
            "গবেষণায় পুনঃমুদ্রণ ফি ৫০ টাকা "
            "উল্লেখ আছে; বর্তমান সরকারি তফসিল "
            "যাচাই প্রয়োজন।",
        ),
        process=(
            "প্রথমে বিদ্যমান নিবন্ধনের রেকর্ড "
            "শনাক্ত করার চেষ্টা করুন।",
            "শুধু সনদের কপি হারিয়ে গেলে নতুন "
            "জন্মনিবন্ধন না করে পুনঃমুদ্রণের "
            "বর্তমান পদ্ধতি অনুসরণ করুন।",
            "নিবন্ধন নম্বর না জানলে সংশ্লিষ্ট "
            "নিবন্ধক কার্যালয়ে রেকর্ড খোঁজার "
            "পদ্ধতি জানতে হবে।",
        ),
        notes=(
            "নতুন নিবন্ধন করলে duplicate record-এর "
            "ঝুঁকি তৈরি হতে পারে।",
            "GD-সংক্রান্ত কোনো বাধ্যতামূলক "
            "শর্ত এই গাইডে অন্তর্ভুক্ত নয়।",
        ),
    ),
    MunicipalServiceGuide(
        key="death_registration",
        title_bn="মৃত্যু নিবন্ধন ও মৃত্যু সনদ",
        department_bn="জন্ম ও মৃত্যু নিবন্ধন শাখা",
        documents=(
            "মৃত ব্যক্তির NID অথবা "
            "জন্মনিবন্ধনের তথ্য।",
            "হাসপাতালে মৃত্যু হলে হাসপাতালের "
            "মৃত্যু-সংক্রান্ত নথি।",
            "বাড়িতে মৃত্যু হলে স্থানীয়ভাবে "
            "গ্রহণযোগ্য প্রত্যয়নপত্রের তথ্য "
            "নিবন্ধক কার্যালয়ে যাচাই করতে হবে।",
            "আবেদনকারী পরিবারের সদস্যের "
            "NID ও যোগাযোগের তথ্য।",
            "দাফন/সৎকারের প্রমাণ প্রযোজ্য "
            "ক্ষেত্রে চাওয়া হতে পারে।",
        ),
        fees=(
            "গবেষণায় উল্লিখিত: ৪৫ দিন পর্যন্ত "
            "বিনামূল্যে, পরবর্তী বয়সসীমায় "
            "২৫ বা ৫০ টাকা।",
            "সংশোধন ও তারিখ সংশোধনের "
            "ফি আলাদাভাবে যাচাই প্রয়োজন।",
        ),
        process=(
            "মৃত্যুর তথ্য ও গ্রহণযোগ্য "
            "মৃত্যু-প্রমাণ সংগ্রহ করুন।",
            "সংশ্লিষ্ট নিবন্ধকের বর্তমান "
            "আবেদনপদ্ধতি অনুসরণ করুন।",
        ),
    ),
    MunicipalServiceGuide(
        key="trade_license",
        title_bn="ট্রেড লাইসেন্স — নতুন ও নবায়ন",
        department_bn="লাইসেন্স শাখা / রাজস্ব বিভাগ",
        documents=(
            "নির্ধারিত আবেদন ফর্ম, মালিকের "
            "NID ও ছবি।",
            "নিজস্ব ব্যবসাস্থলে মালিকানার দলিল; "
            "ভাড়া হলে ভাড়ার চুক্তিপত্র "
            "এবং ঠিকানার সহায়ক নথি।",
            "e-TIN প্রযোজ্য ক্ষেত্রে।",
            "কোম্পানি বা অংশীদারি ব্যবসায় "
            "RJSC/অংশীদারি-সংক্রান্ত দলিল "
            "প্রযোজ্য হতে পারে।",
            "কারখানা, রেস্তোরাঁ বা ঝুঁকিপূর্ণ "
            "ব্যবসায় সংশ্লিষ্ট regulator-এর "
            "অনুমোদন প্রযোজ্য হতে পারে।",
            "নবায়নে পুরোনো লাইসেন্স এবং "
            "হালনাগাদ প্রয়োজনীয় কাগজপত্র।",
        ),
        fees=(
            "লাইসেন্স ফি ব্যবসার ধরন, "
            "ক্যাটাগরি এবং স্থানীয় পৌরসভার "
            "তফসিল অনুযায়ী পরিবর্তিত হতে পারে।",
            "সাইনবোর্ড-সংক্রান্ত চার্জ, কর বা "
            "ভ্যাট প্রযোজ্য কি না যাচাই করুন।",
        ),
        process=(
            "নতুন আবেদন নাকি নবায়ন, "
            "প্রথমে তা নির্ধারণ করুন।",
            "ব্যবসার ধরন ও পৌরসভা অনুযায়ী "
            "লাইসেন্স শাখার checklist সংগ্রহ করুন।",
            "সংশ্লিষ্ট দপ্তরের আবেদন ও "
            "ফি পরিশোধের বর্তমান পদ্ধতি অনুসরণ করুন।",
        ),
        notes=(
            "নবায়নের নির্দিষ্ট সময়সীমা এবং "
            "অর্থবছরভিত্তিক নিয়ম স্থানীয় "
            "নির্দেশনা দিয়ে নিশ্চিত করতে হবে।",
        ),
    ),
    MunicipalServiceGuide(
        key="citizen_heir_certificates",
        title_bn="নাগরিকত্ব, চারিত্রিক ও ওয়ারিশ সনদ",
        department_bn=(
            "সাধারণ প্রশাসন শাখা / "
            "সংশ্লিষ্ট ওয়ার্ড কার্যালয়"
        ),
        documents=(
            "আবেদনকারীর NID অথবা "
            "জন্মনিবন্ধনের তথ্য।",
            "ঠিকানার প্রমাণ এবং "
            "প্রযোজ্য ক্ষেত্রে ছবি।",
            "ওয়ারিশ সনদে মৃত ব্যক্তির "
            "মৃত্যু নিবন্ধন ও সম্ভাব্য "
            "ওয়ারিশদের পরিচয় এবং সম্পর্কের তথ্য।",
            "ভাড়াটিয়ার ক্ষেত্রে ঠিকানার "
            "বিকল্প প্রমাণ সম্পর্কে "
            "ওয়ার্ড কার্যালয়ে যাচাই প্রয়োজন।",
        ),
        fees=(
            "স্থানীয় পৌরসভার Citizen Charter "
            "অনুযায়ী ফি নির্ধারিত হয়।",
            "গবেষণায় বিনামূল্যে থেকে ৫০–২০০ "
            "টাকার পরিসর উল্লেখ আছে; এটি "
            "কোনো নির্দিষ্ট পৌরসভার confirmed fee নয়।",
        ),
        process=(
            "কোন ধরনের সনদ প্রয়োজন তা "
            "নির্দিষ্ট করুন।",
            "সংশ্লিষ্ট ওয়ার্ড বা প্রশাসন শাখার "
            "বর্তমান আবেদন ফর্ম ও checklist যাচাই করুন।",
        ),
    ),
    MunicipalServiceGuide(
        key="holding_tax",
        title_bn="হোল্ডিং নম্বর, নামজারি ও হোল্ডিং ট্যাক্স",
        department_bn="কর নির্ধারণ ও আদায় শাখা",
        documents=(
            "জমির মালিকানার দলিল ও "
            "নামজারি খতিয়ানের কপি।",
            "মালিকের পরিচয়পত্র।",
            "প্রযোজ্য ক্ষেত্রে অনুমোদিত "
            "ভবন নকশা।",
            "হোল্ডিং নাম পরিবর্তনে পূর্ববর্তী "
            "কর পরিশোধের রশিদ প্রাসঙ্গিক হতে পারে।",
        ),
        fees=(
            "কর ভবনের ব্যবহার, মূল্যায়ন "
            "এবং স্থানীয় কর তফসিল অনুযায়ী "
            "নির্ধারিত হতে পারে।",
            "নির্দিষ্ট holding information "
            "ছাড়া নির্ভুল অঙ্ক বলা যাবে না।",
        ),
        process=(
            "নতুন holding, নাম পরিবর্তন "
            "নাকি tax payment—সেবার ধরন নির্ধারণ করুন।",
            "রাজস্ব বিভাগের বর্তমান "
            "আবেদন ও মূল্যায়ন পদ্ধতি যাচাই করুন।",
        ),
    ),
    MunicipalServiceGuide(
        key="building_plan_approval",
        title_bn="ভবন নির্মাণ নকশা অনুমোদন",
        department_bn=(
            "প্রকৌশল / নগর পরিকল্পনা শাখা "
            "অথবা সংশ্লিষ্ট উন্নয়ন কর্তৃপক্ষ"
        ),
        documents=(
            "জমির দলিল, খতিয়ান এবং "
            "ভূমি উন্নয়ন করের নথি।",
            "প্রযোজ্য স্থপতি/প্রকৌশলীর "
            "প্রস্তুতকৃত নকশা।",
            "মালিকের NID এবং "
            "প্রয়োজনীয় সম্পত্তির তথ্য।",
            "বহুতল বা বিশেষ প্রকল্পে "
            "সয়েল টেস্ট ও NOC প্রযোজ্য হতে পারে।",
        ),
        fees=(
            "নকশার ধরন, ভবনের আয়তন "
            "এবং সংশ্লিষ্ট কর্তৃপক্ষের "
            "তফসিল অনুযায়ী ফি নির্ধারিত হয়।",
        ),
        process=(
            "প্রথমে জমির অবস্থান অনুযায়ী "
            "অনুমোদনকারী কর্তৃপক্ষ নিশ্চিত করুন।",
            "ওই কর্তৃপক্ষের current "
            "building-plan checklist অনুসরণ করুন।",
        ),
        notes=(
            "সব পৌরসভার এলাকায় ভবন অনুমোদনের "
            "দায়িত্ব একই কর্তৃপক্ষের নয়।",
        ),
    ),
    MunicipalServiceGuide(
        key="water_connection",
        title_bn="পানির নতুন সংযোগ ও বিল",
        department_bn=(
            "পানি সরবরাহ শাখা / স্থানীয় "
            "পানি সরবরাহ কর্তৃপক্ষ"
        ),
        documents=(
            "আবেদনকারীর NID।",
            "হোল্ডিং বা গ্রাহক-সংক্রান্ত তথ্য।",
            "মালিকানার প্রমাণ অথবা "
            "ভাড়াটিয়ার ক্ষেত্রে মালিকের অনুমতি "
            "প্রযোজ্য হতে পারে।",
        ),
        fees=(
            "সংযোগের ধরন, পাইপের আকার "
            "এবং স্থানীয় schedule অনুযায়ী "
            "সংযোগ ফি ও জামানত নির্ধারিত হতে পারে।",
        ),
        process=(
            "প্রথমে সংশ্লিষ্ট এলাকায় পৌরসভা "
            "নাকি WASA সেবাদাতা তা নিশ্চিত করুন।",
            "সেবাদাতা কর্তৃপক্ষের বর্তমান "
            "আবেদনপদ্ধতি যাচাই করুন।",
        ),
    ),
    MunicipalServiceGuide(
        key="health_epi_mosquito",
        title_bn="স্বাস্থ্যসেবা, EPI ও মশক নিয়ন্ত্রণ",
        department_bn="স্বাস্থ্য বিভাগ / সংশ্লিষ্ট স্বাস্থ্য কর্তৃপক্ষ",
        documents=(
            "শিশুর টিকাদানে জন্মসংক্রান্ত "
            "তথ্য ও অভিভাবকের যোগাযোগের "
            "তথ্য প্রাসঙ্গিক হতে পারে।",
            "অন্যান্য স্বাস্থ্যসেবার নথি "
            "সেবার ধরন অনুযায়ী নির্ভর করে।",
        ),
        fees=(
            "গবেষণায় EPI টিকাদান ও মশক "
            "নিয়ন্ত্রণ বিনামূল্যে উল্লেখ আছে।",
            "স্থানীয় সেবার প্রাপ্যতা ও "
            "প্রযোজ্য চার্জ যাচাই করতে হবে।",
        ),
        process=(
            "সংশ্লিষ্ট এলাকার EPI কেন্দ্র, "
            "স্বাস্থ্য বিভাগ অথবা মশক "
            "নিয়ন্ত্রণ শাখার সঙ্গে যোগাযোগ করুন।",
            "সেবার স্থান, সময় ও "
            "প্রাপ্যতা আগে নিশ্চিত করুন।",
        ),
    ),
)


COMPLAINT_ROUTING_RESEARCH: tuple[tuple[str, str], ...] = (
    ("ময়লা-আবর্জনা", "বর্জ্য ব্যবস্থাপনা বিভাগ"),
    ("ড্রেন জ্যাম / জলাবদ্ধতা", "প্রকৌশল / বর্জ্য বিভাগ"),
    ("পানি সরবরাহ / পাইপ লিকেজ", "পানি সরবরাহ শাখা"),
    ("সড়কবাতি নষ্ট", "বিদ্যুৎ / প্রকৌশল শাখা"),
    ("রাস্তা ভাঙা / গর্ত", "প্রকৌশল বিভাগ"),
    ("মশার উপদ্রব", "স্বাস্থ্য / মশক নিয়ন্ত্রণ শাখা"),
    ("মৃত পশু অপসারণ", "স্বাস্থ্য / বর্জ্য বিভাগ"),
    ("অনুমোদনহীন নির্মাণ", "নগর পরিকল্পনা / প্রকৌশল বিভাগ"),
)


def get_service_guides() -> tuple[MunicipalServiceGuide, ...]:
    return SERVICE_GUIDES


def get_service_guide(
    key: str,
) -> MunicipalServiceGuide | None:
    return next(
        (
            guide
            for guide in SERVICE_GUIDES
            if guide.key == key
        ),
        None,
    )


def render_service_guide(
    guide: MunicipalServiceGuide,
) -> str:
    """
    Render one research guide for human review.

    Not intended for public RAG ingestion before review.
    """
    sections = [
        f"## {guide.title_bn}",
        "",
        f"**Document key:** `{guide.key}`",
        "",
        "**Source status:** RESEARCH — NOT VERIFIED",
        "",
        f"**সংশ্লিষ্ট দপ্তর:** {guide.department_bn}",
        "",
    ]

    for heading, items in (
        ("প্রয়োজনীয় কাগজপত্র", guide.documents),
        ("ফি-সংক্রান্ত গবেষণা", guide.fees),
        ("আবেদন / সেবা গ্রহণের নির্দেশনা", guide.process),
        ("বিশেষ সতর্কতা", guide.notes),
    ):
        if not items:
            continue

        sections.extend(
            [
                f"### {heading}",
                "",
                *[f"- {item}" for item in items],
                "",
            ]
        )

    return "\n".join(sections).rstrip() + "\n"


def build_master_research_document() -> str:
    lines = [
        "# JonoSeba — Municipal Service Master Research",
        "",
        "**Status: UNPUBLISHED / HUMAN REVIEW REQUIRED**",
        "",
        "This document is based on user-provided research "
        "collected from government websites.",
        "",
        "Exact official source excerpts, effective dates "
        "and local applicability are not yet attached.",
        "",
        "Do not present these claims as independently "
        "authenticated government requirements.",
        "",
        "Do not publish this document directly to RAG "
        "without the existing evidence-review process.",
        "",
        "---",
        "",
    ]

    for guide in SERVICE_GUIDES:
        lines.extend(
            [
                render_service_guide(guide).rstrip(),
                "",
                "---",
                "",
            ]
        )

    lines.extend(
        [
            "## অভিযোগের সম্ভাব্য দপ্তর ম্যাপিং",
            "",
            "**Important:** Actual complaint routing must use "
            "active departments from the JonoSeba database.",
            "",
        ]
    )

    for issue, department in COMPLAINT_ROUTING_RESEARCH:
        lines.append(f"- {issue}: {department}")

    lines.extend(
        [
            "",
            "অভিযোগের জন্য প্রয়োজনীয় তথ্য: ওয়ার্ড নম্বর, "
            "সুনির্দিষ্ট অবস্থান, সমস্যার বিবরণ "
            "ও প্রাসঙ্গিক যোগাযোগের তথ্য।",
            "",
            "অভিযোগ ডাটাবেজে সফলভাবে সংরক্ষিত না হলে "
            "জমা হয়েছে বলে জানানো যাবে না।",
            "",
            "Password, OTP বা financial PIN "
            "কখনো সংগ্রহ করা যাবে না।",
            "",
        ]
    )

    return "\n".join(lines)


def save_master_research_document(
    output_path: Path = DEFAULT_OUTPUT_PATH,
) -> Path:
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        build_master_research_document(),
        encoding="utf-8",
    )

    return output_path


def main() -> None:
    output_path = save_master_research_document()

    print("Master research document created:")
    print(output_path)
    print(f"Service guides: {len(SERVICE_GUIDES)}")
    print("Status: UNPUBLISHED / HUMAN REVIEW REQUIRED")


if __name__ == "__main__":
    main()


# Apply the complete JonoSeba citizen-service master knowledge.
from app.modules.knowledge.full_service_data import (
    enrich_catalog as _enrich_catalog,
)

SERVICE_GUIDES = _enrich_catalog(SERVICE_GUIDES)
