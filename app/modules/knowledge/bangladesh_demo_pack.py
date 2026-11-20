from dataclasses import dataclass
from app.modules.knowledge.ingestion import (
    KnowledgeDocumentInput,
)
from app.modules.knowledge.models import KnowledgeLanguage

@dataclass(frozen=True)
class DraftKnowledgeGuide:
    document_key: str
    title: str
    content: str
    review_flags: tuple[str, ...]

    def to_ingestion_input(self) -> KnowledgeDocumentInput:
        """
        Convert a draft guide into an unpublished document.

        Source URL and verification timestamp remain empty
        until an authorized human reviews the evidence.
        """
        return KnowledgeDocumentInput(
            document_key=self.document_key,
            document_title=self.title,
            content=self.content,
            language=KnowledgeLanguage.BANGLA,
            source_url=None,
            source_name=None,
            verified_at=None,
            is_published=False,
        )


DRAFT_GUIDES: tuple[DraftKnowledgeGuide, ...] = (
    DraftKnowledgeGuide(
        document_key="bd-birth-registration-new",
        title="নতুন জন্মনিবন্ধন: আবেদন ও প্রয়োজনীয় কাগজপত্র",
        content=(
            "নতুন জন্মনিবন্ধনের জন্য BDRIS পোর্টালে আবেদন "
            "এবং সংশ্লিষ্ট নিবন্ধক কার্যালয়ে প্রয়োজনীয় "
            "কাগজপত্র জমা দেওয়ার প্রক্রিয়া থাকতে পারে। "
            "আবেদনের ক্ষেত্রে শিশুর বয়স গুরুত্বপূর্ণ।\n\n"
            "নবজাতক ও পাঁচ বছরের কম বয়সী শিশুর জন্য "
            "EPI টিকাদান কার্ড, হাসপাতালের জন্মসংক্রান্ত "
            "কাগজ, পিতা-মাতার পরিচয় বা জন্মনিবন্ধনের তথ্য "
            "এবং ঠিকানার প্রমাণ চাওয়া হতে পারে।\n\n"
            "পাঁচ বছরের বেশি বয়সীদের ক্ষেত্রে শিক্ষাগত "
            "সনদ, শিক্ষাপ্রতিষ্ঠানের প্রত্যয়নপত্র অথবা "
            "গ্রহণযোগ্য বয়স-প্রমাণের অন্যান্য দলিল "
            "প্রাসঙ্গিক হতে পারে।\n\n"
            "পিতা-মাতার ১৭ ডিজিটের জন্মনিবন্ধন নম্বর, "
            "NID, হোল্ডিং ট্যাক্সের রশিদ এবং "
            "আবেদন জমার সময়সীমা সম্পর্কে নির্দিষ্ট নিয়ম "
            "আবেদনকারীর পরিস্থিতি অনুযায়ী যাচাই করতে হবে।\n\n"
            "এটি ব্যবহারকারীর সংগৃহীত তথ্যের খসড়া। "
            "এখনো সরকারি নির্দেশিকা হিসেবে অনুমোদিত নয়।"
        ),
        review_flags=(
            "Age-based mandatory documents",
            "Parents' birth registration versus NID rules",
            "Holding tax requirements",
            "Application submission deadline",
        ),
    ),
    DraftKnowledgeGuide(
        document_key="bd-birth-registration-correction",
        title="জন্মনিবন্ধন সংশোধন: নাম, জন্মতারিখ ও অন্যান্য তথ্য",
        content=(
            "জন্মনিবন্ধনের নাম, বাংলা বা ইংরেজি বানান, "
            "জন্মতারিখ, পিতা-মাতার নাম অথবা ঠিকানা "
            "সংশোধনের জন্য আলাদা প্রমাণপত্র প্রয়োজন হতে পারে।\n\n"
            "নাম সংশোধনে শিক্ষাগত সনদ, NID, পাসপোর্ট "
            "বা শিশুর ক্ষেত্রে EPI কার্ড সহায়ক হতে পারে। "
            "জন্মতারিখ সংশোধনে হাসপাতালের জন্মসংক্রান্ত "
            "প্রমাণ অথবা শিক্ষাগত সনদ গুরুত্বপূর্ণ হতে পারে।\n\n"
            "পিতা-মাতার নাম সংশোধনে তাদের নিজস্ব "
            "পরিচয়পত্র ও জন্মনিবন্ধনের তথ্য প্রয়োজন "
            "হতে পারে। ঠিকানা সংশোধনে হোল্ডিং ট্যাক্সের "
            "রশিদ, ইউটিলিটি বিল বা বাসিন্দা সনদ "
            "প্রাসঙ্গিক হতে পারে।\n\n"
            "BDRIS সংশোধন পোর্টাল, প্রমাণপত্র আপলোডের "
            "সীমা, সর্বোচ্চ সংশোধনের সংখ্যা এবং "
            "উচ্চতর কর্তৃপক্ষের অনুমোদনসংক্রান্ত নিয়ম "
            "অবশ্যই বর্তমান সরকারি নির্দেশিকা দিয়ে "
            "যাচাই করতে হবে।\n\n"
            "এটি review-pending খসড়া তথ্য।"
        ),
        review_flags=(
            "Correction application process",
            "Three-correction limit claim",
            "Upload size and document formats",
            "Authority approval requirements",
        ),
    ),
    DraftKnowledgeGuide(
        document_key="bd-lost-birth-certificate",
        title="জন্মসনদ হারিয়ে গেলে কী করবেন",
        content=(
            "জন্মসনদ হারিয়ে গেলে আগে বিদ্যমান "
            "জন্মনিবন্ধন রেকর্ড খুঁজে বের করার বিষয়টি "
            "বিবেচনা করা উচিত। শুধু কাগজ হারানোর কারণে "
            "দ্বিতীয় জন্মনিবন্ধন তৈরি করা ঠিক নয়।\n\n"
            "পুরোনো সনদের ছবি বা ফটোকপি, ১৭ ডিজিটের "
            "নম্বর, জন্মতারিখ এবং পরিচয়সংক্রান্ত "
            "সহায়ক কাগজ রেকর্ড খুঁজতে কাজে লাগতে পারে। "
            "নম্বর না জানলে সংশ্লিষ্ট নিবন্ধক "
            "কার্যালয়ের সহায়তা প্রয়োজন হতে পারে।\n\n"
            "BDRIS verification এবং নিবন্ধক কার্যালয় "
            "থেকে সরকারি পুনঃমুদ্রিত সনদ সংগ্রহের "
            "প্রক্রিয়া এক নয়।\n\n"
            "হারানো জন্মসনদে থানায় GD বাধ্যতামূলক "
            "কি না, কী পরিচয়পত্র লাগবে এবং "
            "পুনঃমুদ্রণের ফি কত—এসব স্থানীয় ও "
            "বর্তমান সরকারি নিয়ম দিয়ে যাচাই করতে হবে।\n\n"
            "এটি review-pending খসড়া তথ্য।"
        ),
        review_flags=(
            "Whether GD is mandatory or conditional",
            "Reprint procedure",
            "Duplicate certificate fee",
            "Accepted identity evidence",
        ),
    ),
    DraftKnowledgeGuide(
        document_key="bd-birth-death-registration-fees",
        title="জন্ম ও মৃত্যু নিবন্ধন: ফি যাচাইয়ের খসড়া",
        content=(
            "সংগৃহীত খসড়া তথ্যে জন্মের ৪৫ দিনের "
            "মধ্যে নিবন্ধন বিনামূল্যে, পরে নির্দিষ্ট "
            "বয়সসীমা অনুযায়ী ২৫ অথবা ৫০ টাকা "
            "ফি থাকার দাবি করা হয়েছে।\n\n"
            "জন্মতারিখ সংশোধনে ১০০ টাকা, অন্যান্য "
            "সংশোধনে ৫০ টাকা এবং সনদের নকল কপির "
            "জন্য ৫০ টাকা ফি থাকার দাবিও রয়েছে।\n\n"
            "মৃত্যুনিবন্ধনের ক্ষেত্রে সময়ের ব্যবধান "
            "অনুযায়ী পৃথক ফি থাকার তথ্য দেওয়া হয়েছে।\n\n"
            "এই টাকার অঙ্কগুলো এখনো বর্তমান সরকারি "
            "ফি তফসিলের সঙ্গে মিলিয়ে দেখা হয়নি। "
            "বিদেশে আবেদনের কিছু ফি-সংক্রান্ত "
            "তথ্য পরস্পর অসংগত।\n\n"
            "এই খসড়া সরকারি ফি ঘোষণা নয়। "
            "নির্দিষ্ট ফি নাগরিককে নিশ্চিত করার "
            "আগে সরকারি তফসিল যাচাই করতে হবে।"
        ),
        review_flags=(
            "All domestic fee amounts",
            "Overseas fee inconsistencies",
            "Free certificate versus paid reprint",
            "Effective date of fee schedule",
        ),
    ),
    DraftKnowledgeGuide(
        document_key="bd-trade-license",
        title="ট্রেড লাইসেন্স: আবেদন ও কাগজপত্র",
        content=(
            "ট্রেড লাইসেন্সের জন্য ব্যবসার অবস্থান, "
            "মালিকানার ধরন এবং ব্যবসার ক্যাটাগরি "
            "নির্ধারণ গুরুত্বপূর্ণ।\n\n"
            "একক মালিকানাধীন ব্যবসার ক্ষেত্রে মালিকের "
            "NID, ছবি, ব্যবসার ঠিকানার প্রমাণ, "
            "ভাড়ার চুক্তিপত্র অথবা মালিকানার দলিল "
            "প্রাসঙ্গিক হতে পারে।\n\n"
            "কোম্পানির ক্ষেত্রে RJSC নিবন্ধন, "
            "পরিচালকদের তথ্য এবং প্রতিষ্ঠানসংক্রান্ত "
            "কর নথি প্রয়োজন হতে পারে। বিশেষ ধরনের "
            "ব্যবসায় পরিবেশ, অগ্নিনিরাপত্তা বা "
            "অন্যান্য অনুমোদন লাগতে পারে।\n\n"
            "ট্রেড লাইসেন্স ফি সব ব্যবসার জন্য "
            "এক নয়। স্থানীয় কর্তৃপক্ষের ফি তফসিল, "
            "ব্যবসার ধরন এবং প্রযোজ্য কর অনুযায়ী "
            "অঙ্ক নির্ধারিত হতে পারে।\n\n"
            "এটি review-pending খসড়া তথ্য।"
        ),
        review_flags=(
            "Business-type document requirements",
            "Renewal period and penalties",
            "Applicable local fee schedule",
            "Special business approvals",
        ),
    ),
    DraftKnowledgeGuide(
        document_key="bd-death-registration",
        title="মৃত্যু নিবন্ধন: আবেদন ও প্রয়োজনীয় দলিল",
        content=(
            "মৃত্যু নিবন্ধনে মৃত ব্যক্তির পরিচয়, "
            "মৃত্যুর তথ্য এবং আবেদনকারীর পরিচয় "
            "প্রমাণের প্রয়োজন হতে পারে।\n\n"
            "মৃত ব্যক্তির NID বা জন্মনিবন্ধনের তথ্য, "
            "হাসপাতালের মৃত্যুসংক্রান্ত কাগজ, "
            "প্রযোজ্য ক্ষেত্রে চিকিৎসক বা স্থানীয় "
            "কর্তৃপক্ষের প্রত্যয়নপত্র এবং আবেদনকারীর "
            "পরিচয়পত্র প্রাসঙ্গিক হতে পারে।\n\n"
            "আবেদন পদ্ধতি, দাফন বা সৎকারের রশিদ "
            "প্রয়োজন কি না, সময়সীমা এবং নির্ধারিত "
            "ফি সংশ্লিষ্ট নিবন্ধক কর্তৃপক্ষের "
            "বর্তমান নিয়ম দিয়ে যাচাই করতে হবে।\n\n"
            "এটি review-pending খসড়া তথ্য।"
        ),
        review_flags=(
            "Mandatory death evidence",
            "Applicant eligibility",
            "Registration fees and deadlines",
        ),
    ),
    DraftKnowledgeGuide(
        document_key="bd-citizen-heir-certificates",
        title="নাগরিকত্ব, চারিত্রিক ও ওয়ারিশ সনদ",
        content=(
            "নাগরিকত্ব, চারিত্রিক ও ওয়ারিশ সনদের "
            "জন্য স্থানীয় ওয়ার্ড বা দায়িত্বপ্রাপ্ত "
            "কার্যালয়ে আবেদন করতে হতে পারে।\n\n"
            "পরিচয়পত্র, জন্মনিবন্ধন, ছবি এবং "
            "ঠিকানার প্রমাণ প্রাসঙ্গিক হতে পারে। "
            "ওয়ারিশ সনদের জন্য মৃত ব্যক্তির মৃত্যু "
            "সনদ, সম্ভাব্য ওয়ারিশদের পরিচয় এবং "
            "পারিবারিক সম্পর্কের তথ্য লাগতে পারে।\n\n"
            "কোন কাগজ বাধ্যতামূলক এবং কত ফি "
            "প্রযোজ্য, তা সংশ্লিষ্ট স্থানীয় "
            "কর্তৃপক্ষের সিটিজেন চার্টার থেকে "
            "যাচাই করতে হবে।\n\n"
            "এটি review-pending খসড়া তথ্য।"
        ),
        review_flags=(
            "Certificate-specific requirements",
            "Ward office jurisdiction",
            "Local certificate fees",
        ),
    ),
    DraftKnowledgeGuide(
        document_key="bd-holding-tax-water",
        title="হোল্ডিং ট্যাক্স ও নতুন পানি সংযোগ",
        content=(
            "নতুন হোল্ডিং নম্বর, মালিকানা পরিবর্তন "
            "এবং হোল্ডিং ট্যাক্সের জন্য রাজস্ব "
            "শাখা প্রাসঙ্গিক হতে পারে। জমির দলিল, "
            "নামজারি খতিয়ান, মালিকের পরিচয়পত্র "
            "ও পুরোনো কর রশিদ প্রয়োজন হতে পারে।\n\n"
            "নতুন পানি সংযোগের জন্য NID, হোল্ডিং "
            "তথ্য, ঠিকানার প্রমাণ এবং মালিকের "
            "অনুমতিপত্র প্রাসঙ্গিক হতে পারে।\n\n"
            "পানি সরবরাহের কর্তৃপক্ষ সব জায়গায় "
            "এক নয়; কোথাও পৃথক WASA দায়িত্বপ্রাপ্ত। "
            "সংযোগ ফি, জামানত এবং করের পরিমাণ "
            "এলাকা, সংযোগ ও স্থাপনার ধরন অনুযায়ী "
            "ভিন্ন হতে পারে।\n\n"
            "এটি review-pending খসড়া তথ্য।"
        ),
        review_flags=(
            "Responsible authority by municipality",
            "Connection and holding fees",
            "Mandatory property documents",
        ),
    ),
    DraftKnowledgeGuide(
        document_key="bd-building-health-services",
        title="ভবন অনুমোদন ও পৌর স্বাস্থ্যসেবা",
        content=(
            "ভবনের নকশা অনুমোদনের দায়িত্ব "
            "স্থানভেদে পৌরসভা বা সংশ্লিষ্ট "
            "উন্নয়ন কর্তৃপক্ষের হতে পারে। "
            "জমির দলিল, খতিয়ান, অনুমোদনযোগ্য "
            "নকশা এবং প্রকৌশলগত প্রমাণ "
            "প্রাসঙ্গিক হতে পারে।\n\n"
            "স্থানীয় স্বাস্থ্যসেবায় টিকাদান, "
            "মশক নিয়ন্ত্রণ এবং প্রাথমিক "
            "জনস্বাস্থ্য-সংক্রান্ত কার্যক্রম "
            "থাকতে পারে।\n\n"
            "নির্দিষ্ট অফিসের এখতিয়ার, "
            "লাইসেন্স, ফি ও সেবার প্রাপ্যতা "
            "স্থানীয় সরকারি নথি দিয়ে "
            "যাচাই করতে হবে।\n\n"
            "এটি review-pending খসড়া তথ্য।"
        ),
        review_flags=(
            "Development authority jurisdiction",
            "Building approval requirements",
            "Local health service availability",
        ),
    ),
    DraftKnowledgeGuide(
        document_key="bd-municipal-complaint-routing",
        title="পৌরসভার অভিযোগ: সমস্যা ও সংশ্লিষ্ট বিভাগ",
        content=(
            "ময়লা-আবর্জনার অভিযোগ বর্জ্য "
            "ব্যবস্থাপনা বিভাগের সঙ্গে সম্পর্কিত "
            "হতে পারে। নষ্ট রাস্তা ও ড্রেন "
            "প্রকৌশল বা ড্রেনেজ বিভাগের সঙ্গে "
            "সম্পর্কিত হতে পারে।\n\n"
            "পানি সরবরাহ সমস্যা পানি সরবরাহ "
            "বিভাগে, নষ্ট রাস্তার বাতি "
            "স্ট্রিট লাইটিং বিভাগে এবং "
            "মশার উপদ্রব জনস্বাস্থ্য বিভাগে "
            "জানানো প্রাসঙ্গিক হতে পারে।\n\n"
            "অভিযোগের জন্য সমস্যা, সুনির্দিষ্ট "
            "ঠিকানা বা ল্যান্ডমার্ক, কতদিন ধরে "
            "সমস্যা হচ্ছে এবং প্রযোজ্য ক্ষেত্রে "
            "ওয়ার্ড নম্বর সহায়ক তথ্য।\n\n"
            "JonoSeba-তে বাস্তব বিভাগ নির্ধারণে "
            "active departments database ব্যবহার "
            "করতে হবে; এই খসড়াকে স্থির "
            "department mapping হিসেবে ধরবে না।\n\n"
            "অভিযোগ জমা হয়েছে বলে নিশ্চিত "
            "করার আগে backend complaint record "
            "সফলভাবে তৈরি হওয়া প্রয়োজন।"
        ),
        review_flags=(
            "Municipality-specific department mapping",
            "Complaint form required fields",
            "Automatic submission capability",
        ),
    ),
)


def get_draft_guides() -> tuple[DraftKnowledgeGuide, ...]:
    return DRAFT_GUIDES
