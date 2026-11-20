from dataclasses import dataclass
from typing import Literal


RiskLevel = Literal["normal", "high", "critical"]


@dataclass(frozen=True)
class ResearchClaim:
    """
    A user-supplied research claim awaiting verification.

    No claim in this catalog is official or approved.
    """

    claim_id: str
    topic: str
    text_bn: str
    risk: RiskLevel
    verification_question: str
    source_url: str | None = None
    verified: bool = False


def claim(
    claim_id: str,
    topic: str,
    text_bn: str,
    risk: RiskLevel,
    verification_question: str,
) -> ResearchClaim:
    return ResearchClaim(
        claim_id=claim_id,
        topic=topic,
        text_bn=text_bn,
        risk=risk,
        verification_question=verification_question,
    )


RESEARCH_CLAIMS: tuple[ResearchClaim, ...] = (
    # NEW BIRTH REGISTRATION
    claim(
        "BR-001",
        "birth_registration",
        "নতুন জন্মনিবন্ধনের জন্য BDRIS-এর মাধ্যমে "
        "আবেদন এবং সংশ্লিষ্ট নিবন্ধক কার্যালয়ে "
        "কাগজপত্র জমা দেওয়ার পদ্ধতি রয়েছে।",
        "high",
        "বর্তমান সরকারি আবেদন পদ্ধতি ও জমার নিয়ম কী?",
    ),
    claim(
        "BR-002",
        "birth_registration",
        "০–৪৫ দিনের শিশুর ক্ষেত্রে EPI কার্ড, "
        "হাসপাতালের কাগজ, অভিভাবকের পরিচয় "
        "এবং ঠিকানার প্রমাণ চাওয়া হতে পারে।",
        "high",
        "এই বয়সে কোন নথি বাধ্যতামূলক এবং "
        "কোনটি বিকল্প বা পরিস্থিতিভেদে প্রযোজ্য?",
    ),
    claim(
        "BR-003",
        "birth_registration",
        "৪৬ দিন থেকে পাঁচ বছর বয়সে EPI কার্ড, "
        "জন্মের প্রমাণ, অভিভাবকের পরিচয় ও "
        "প্রযোজ্য ক্ষেত্রে স্কুলের প্রত্যয়নপত্র "
        "চাওয়া হতে পারে।",
        "high",
        "এই বয়সসীমার বর্তমান সরকারি document list কী?",
    ),
    claim(
        "BR-004",
        "birth_registration",
        "পাঁচ বছরের বেশি বয়সে শিক্ষাগত সনদ, "
        "প্রতিষ্ঠানপ্রধানের প্রত্যয়নপত্র অথবা "
        "গ্রহণযোগ্য বয়স-প্রমাণের দলিল প্রাসঙ্গিক।",
        "high",
        "কোন বয়স-প্রমাণের নথিগুলো সরকার গ্রহণ করে?",
    ),
    claim(
        "BR-005",
        "birth_registration",
        "২০০১ সালের ১ জানুয়ারির পরে জন্মগ্রহণকারীর "
        "ক্ষেত্রে পিতা-মাতার ১৭ ডিজিটের "
        "জন্মনিবন্ধন বাধ্যতামূলক—এমন দাবি "
        "সংগৃহীত গবেষণায় রয়েছে।",
        "critical",
        "দাবিটির সঠিক আইনগত ভিত্তি, শর্ত এবং "
        "ব্যতিক্রম কী? আবেদনকারীর জন্মসাল ও "
        "পিতা-মাতার জন্মসালের নিয়ম কি আলাদা?",
    ),
    claim(
        "BR-006",
        "birth_registration",
        "হোল্ডিং ট্যাক্স রশিদ ঠিকানার প্রমাণ "
        "হিসেবে চাওয়া হতে পারে। ভাড়াটিয়া বা "
        "নিজস্ব হোল্ডিং নেই এমন আবেদনকারীর "
        "ক্ষেত্রে বিকল্প প্রমাণ প্রয়োজন হতে পারে।",
        "high",
        "হোল্ডিং ট্যাক্স কি সর্বজনীন বাধ্যতামূলক "
        "নাকি একাধিক গ্রহণযোগ্য ঠিকানা-প্রমাণের একটি?",
    ),

    # CORRECTION
    claim(
        "BC-001",
        "birth_correction",
        "নাম বা বানান সংশোধনে শিক্ষা সনদ, "
        "NID, পাসপোর্ট, EPI কার্ড অথবা "
        "জন্মসংক্রান্ত দলিল প্রাসঙ্গিক হতে পারে।",
        "high",
        "কোন বয়সে ও কোন সংশোধনে কোন প্রমাণ গ্রহণযোগ্য?",
    ),
    claim(
        "BC-002",
        "birth_correction",
        "জন্মতারিখ সংশোধনে শিক্ষা সনদ, "
        "হাসপাতালের জন্মসংক্রান্ত নথি "
        "অথবা অন্যান্য গ্রহণযোগ্য প্রমাণ লাগে।",
        "high",
        "বর্তমান জন্মতারিখ সংশোধনের প্রমাণ ও "
        "অনুমোদন-সংক্রান্ত বিধান কী?",
    ),
    claim(
        "BC-003",
        "birth_correction",
        "পিতা-মাতার নাম সংশোধনে তাঁদের পরিচয় "
        "ও জন্মনিবন্ধনের তথ্য এবং সম্পর্কের "
        "সহায়ক প্রমাণ প্রয়োজন হতে পারে।",
        "high",
        "পিতা-মাতার রেকর্ড সংশোধন ও mapping "
        "কখন আগে করতে হয়?",
    ),
    claim(
        "BC-004",
        "birth_correction",
        "একটি জন্মনিবন্ধন সর্বোচ্চ তিনবার "
        "সংশোধন করা যায়—এমন দাবি রয়েছে।",
        "critical",
        "বর্তমান সরকারি BDRIS বিধিতে সত্যিই কি "
        "সর্বোচ্চ তিনবারের সীমা রয়েছে?",
    ),

    # LOST CERTIFICATE
    claim(
        "BL-001",
        "lost_birth_certificate",
        "জন্মসনদের কাগজ হারিয়ে গেলে বিদ্যমান "
        "নিবন্ধনের রেকর্ড খুঁজে পুনঃমুদ্রণের "
        "পথ অনুসরণ করা উচিত; নতুন নিবন্ধন "
        "করলে duplicate record-এর ঝুঁকি রয়েছে।",
        "high",
        "বর্তমান official reprint procedure কী?",
    ),
    claim(
        "BL-002",
        "lost_birth_certificate",
        "পুরোনো সনদের ছবি, নম্বর, জন্মতারিখ "
        "ও পরিচয়পত্র রেকর্ড খুঁজতে সহায়ক হতে পারে।",
        "normal",
        "নম্বর না জানা থাকলে official record "
        "recovery-এর পদ্ধতি কী?",
    ),
    claim(
        "BL-003",
        "lost_birth_certificate",
        "হারানো জন্মসনদের জন্য থানার GD "
        "প্রয়োজন হতে পারে—তবে এটি সব ক্ষেত্রে "
        "বাধ্যতামূলক কি না নিশ্চিত নয়।",
        "critical",
        "সরকারি নকল সনদ পেতে GD বাধ্যতামূলক "
        "নাকি বিশেষ পরিস্থিতিতে প্রয়োজন?",
    ),

    # REGISTRATION FEES
    claim(
        "FEE-001",
        "registration_fees",
        "সংগৃহীত তথ্য অনুযায়ী নতুন জন্মনিবন্ধনে "
        "৪৫ দিন পর্যন্ত বিনামূল্যে, ৪৬ দিন "
        "থেকে পাঁচ বছর ২৫ টাকা এবং "
        "পাঁচ বছরের পরে ৫০ টাকা ফি-এর দাবি আছে।",
        "critical",
        "বর্তমান সরকারি ফি তফসিল, কার্যকর তারিখ "
        "এবং বয়সসীমার সঠিক ব্যাখ্যা কী?",
    ),
    claim(
        "FEE-002",
        "registration_fees",
        "সংগৃহীত তথ্য অনুযায়ী জন্মতারিখ সংশোধন "
        "১০০ টাকা, অন্যান্য সংশোধন ৫০ টাকা "
        "এবং নকল সনদ ৫০ টাকা হওয়ার দাবি আছে।",
        "critical",
        "বর্তমান সংশোধন ও পুনঃমুদ্রণ ফি তফসিল কী?",
    ),

    # DEATH REGISTRATION
    claim(
        "DR-001",
        "death_registration",
        "মৃত্যু নিবন্ধনে মৃত ব্যক্তির পরিচয়, "
        "মৃত্যুর প্রমাণ, আবেদনকারীর পরিচয় "
        "এবং পরিস্থিতিভেদে অন্যান্য দলিল "
        "প্রাসঙ্গিক হতে পারে।",
        "high",
        "হাসপাতাল ও বাড়িতে মৃত্যুর ক্ষেত্রে "
        "সঠিক বাধ্যতামূলক কাগজপত্র কী?",
    ),
    claim(
        "DR-002",
        "death_registration",
        "মৃত্যু নিবন্ধনের ফি সময়সীমা অনুযায়ী "
        "বিনামূল্যে, ২৫ টাকা বা ৫০ টাকা—"
        "এমন তথ্য সংগৃহীত হয়েছে।",
        "critical",
        "বর্তমান সরকারি death-registration "
        "ফি ও সংশোধন ফি কী?",
    ),

    # TRADE LICENSE
    claim(
        "TL-001",
        "trade_license",
        "ট্রেড লাইসেন্সে মালিকের পরিচয়, ছবি, "
        "ব্যবসার ঠিকানা, মালিকানা বা ভাড়ার "
        "দলিল এবং প্রযোজ্য কর নথি লাগতে পারে।",
        "high",
        "একক মালিকানা, অংশীদারি ও কোম্পানির "
        "জন্য স্থানীয় official checklist কী?",
    ),
    claim(
        "TL-002",
        "trade_license",
        "কোম্পানির ক্ষেত্রে RJSC নথি এবং "
        "কারখানা বা ঝুঁকিপূর্ণ ব্যবসায় "
        "অতিরিক্ত অনুমোদন প্রযোজ্য হতে পারে।",
        "high",
        "কোন ব্যবসায় কোন regulator-এর "
        "অনুমোদন বাধ্যতামূলক?",
    ),
    claim(
        "TL-003",
        "trade_license",
        "ট্রেড লাইসেন্স ফি ব্যবসার ক্যাটাগরি, "
        "স্থানীয় কর্তৃপক্ষ এবং প্রযোজ্য "
        "কর বা চার্জ অনুযায়ী পরিবর্তিত হয়।",
        "high",
        "নির্দিষ্ট পৌরসভার বর্তমান fee schedule "
        "এবং renewal deadline কী?",
    ),

    # CITIZEN AND HEIR CERTIFICATES
    claim(
        "CERT-001",
        "citizen_certificates",
        "নাগরিকত্ব বা চারিত্রিক সনদে পরিচয়পত্র, "
        "ঠিকানার প্রমাণ ও ছবি লাগতে পারে।",
        "high",
        "প্রতিটি সনদের local citizen charter কী বলে?",
    ),
    claim(
        "CERT-002",
        "citizen_certificates",
        "ওয়ারিশ সনদের ক্ষেত্রে মৃত্যু সনদ, "
        "সম্ভাব্য ওয়ারিশদের পরিচয় এবং "
        "পারিবারিক সম্পর্কের তথ্য প্রয়োজন হতে পারে।",
        "high",
        "ওয়ারিশ যাচাইয়ের official checklist "
        "ও নির্ধারিত ফি কী?",
    ),

    # HOLDING TAX
    claim(
        "HT-001",
        "holding_tax",
        "হোল্ডিং নম্বর বা মালিকানা পরিবর্তনে "
        "জমির দলিল, খতিয়ান, পরিচয়পত্র "
        "এবং আগের কর রশিদ প্রাসঙ্গিক হতে পারে।",
        "high",
        "নির্দিষ্ট পৌরসভার রাজস্ব বিভাগের "
        "নথি ও সঠিক আবেদন প্রক্রিয়া কী?",
    ),
    claim(
        "HT-002",
        "holding_tax",
        "হোল্ডিং ট্যাক্সের পরিমাণ ভবনের ধরন, "
        "মূল্যায়ন ও স্থানীয় কর তফসিলের "
        "ওপর নির্ভর করে।",
        "high",
        "নির্দিষ্ট এলাকার applicable assessment "
        "method ও tax schedule কী?",
    ),

    # BUILDING APPROVAL
    claim(
        "BP-001",
        "building_approval",
        "ভবন অনুমোদনে জমির দলিল, খতিয়ান, "
        "প্রকৌশলগত নকশা এবং প্রযোজ্য ক্ষেত্রে "
        "সয়েল টেস্ট বা NOC লাগতে পারে।",
        "high",
        "এই জমির অবস্থানে কোন কর্তৃপক্ষ "
        "ভবনের নকশা অনুমোদনের দায়িত্বে?",
    ),

    # WATER SUPPLY
    claim(
        "WS-001",
        "water_connection",
        "পানির সংযোগে আবেদনকারীর পরিচয়, "
        "হোল্ডিং তথ্য ও মালিকানার প্রমাণ "
        "বা মালিকের অনুমতি লাগতে পারে।",
        "high",
        "এই এলাকায় পৌরসভা নাকি WASA "
        "সংযোগ দেওয়ার কর্তৃপক্ষ?",
    ),
    claim(
        "WS-002",
        "water_connection",
        "পানির সংযোগ ফি পাইপের আকার, "
        "সংযোগের ধরন ও স্থানীয় কর্তৃপক্ষের "
        "তফসিল অনুযায়ী ভিন্ন হতে পারে।",
        "high",
        "বর্তমান connection fee ও deposit কত?",
    ),

    # HEALTH
    claim(
        "HEALTH-001",
        "health_services",
        "EPI টিকাদান, মশক নিয়ন্ত্রণ এবং "
        "কিছু প্রাথমিক স্বাস্থ্যসেবা সংশ্লিষ্ট "
        "স্থানীয় স্বাস্থ্য কর্তৃপক্ষের মাধ্যমে "
        "পাওয়া যেতে পারে।",
        "high",
        "এই পৌরসভায় কোন service পাওয়া যায়, "
        "কোথায় এবং কী শর্তে?",
    ),

    # COMPLAINTS
    claim(
        "CMP-001",
        "complaint_routing",
        "বর্জ্য, ড্রেন, পানি, রাস্তা, "
        "সড়কবাতি ও জনস্বাস্থ্য অভিযোগের "
        "জন্য আলাদা দায়িত্বপ্রাপ্ত বিভাগ "
        "থাকতে পারে।",
        "normal",
        "JonoSeba database-এর active departments "
        "ও complaint categories-এর mapping কী?",
    ),
    claim(
        "CMP-002",
        "complaint_routing",
        "অভিযোগে সমস্যার বিবরণ, নির্দিষ্ট স্থান "
        "এবং প্রযোজ্য ক্ষেত্রে ওয়ার্ড নম্বর "
        "ও যোগাযোগের তথ্য প্রয়োজন হতে পারে।",
        "normal",
        "বর্তমান complaint API-তে কোন fields "
        "বাস্তবে required?",
    ),
)


def get_research_claims(
    topic: str | None = None,
) -> tuple[ResearchClaim, ...]:
    if topic is None:
        return RESEARCH_CLAIMS

    return tuple(
        item
        for item in RESEARCH_CLAIMS
        if item.topic == topic
    )


def get_pending_critical_claims() -> tuple[ResearchClaim, ...]:
    return tuple(
        item
        for item in RESEARCH_CLAIMS
        if item.risk == "critical" and not item.verified
    )


def get_research_topics() -> tuple[str, ...]:
    return tuple(
        dict.fromkeys(
            item.topic
            for item in RESEARCH_CLAIMS
        )
    )
