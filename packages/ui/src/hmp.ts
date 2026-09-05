
export type Uhub = "en" | "ar";
const S = {
  en: {
    title: "Bayan — declaration before crossing", user: "Acting as", lang: "Language", deployment: "Deployment",
    engineer: "Engineer", reviewer: "Reviewer", lead: "Delivery lead", auditor: "Auditor",
    feasibility: "Ask a question — see its price first", question: "Question", minClass: "Minimum data", achievable: "Achievable", path: "Approval path", realtime: "Real-time", skills: "Certified skills",
    run: "Run", dryrun: "Dry run (free, synthetic)", certificate: "Certificate", gates: "Gates", tracks: "Tracks", releasable: "Releasable now", doesNotStop: "What this grade does not stop", nearest: "Nearest releasable form", expires: "Expires",
    uplift: "Uplift to D2", apply: "Apply", recommended: "recommended", request: "Request release", purpose: "Purpose (your justification, recorded)", sensitiveDeclared: "Sensitive attributes named in the purpose",
    exemplar: "Request one record (exemplar)", records: "Candidate records", upgrade: "Upgrade to D3 (async)", status: "Status", commitment: "Sealed commitment",
    queue: "Review queue — grouped by risk, never by arrival", delta: "What changed", fullBundle: "Show the full bundle", hideBundle: "Hide the full bundle", noPrior: "No comparable earlier release: this is a new shape.",
    accountability: "You are signing as", retention: "Retention", recipient: "Recipient", decide: "Your decision", undecided: "Undecided", reject: "Reject — no reason needed", approve: "Approve…", reason: "Your reason, in your own words", confirmApprove: "Confirm approval of a non-runner", cancel: "Cancel",
    sealed: "The machine's finding is sealed until you have voted.", reveal: "Machine finding (revealed after your vote)", agreement: "You and the machine agree", disagreement: "You and the machine disagree — both are recorded",
    resolve: "Resolve (both votes are in)", waiting: "Waiting for the other reviewer — their vote is blinded from you",
    summary: "Acceptance evidence", register: "Register — every release and every refusal", ledger: "Ledger", bundle: "Bundle", packRules: "Pack rules and provenance", verifyHint: "Verify offline:",
    quarantined: "Quarantined — output did not conform; never downgraded",
  },
  ar: {
    title: "بيان — إقرار قبل العبور", user: "بصفة", lang: "اللغة", deployment: "النشر",
    engineer: "مهندس", reviewer: "مراجع", lead: "قائد التسليم", auditor: "مدقق",
    feasibility: "اطرح سؤالاً — واعرف ثمنه أولاً", question: "السؤال", minClass: "الحد الأدنى من البيانات", achievable: "الدرجة الممكنة", path: "مسار الموافقة", realtime: "فوري", skills: "المهارات المعتمدة",
    run: "تشغيل", dryrun: "تجربة (مجانية، بيانات اصطناعية)", certificate: "الشهادة", gates: "البوابات", tracks: "المسارات", releasable: "قابل للإفراج الآن", doesNotStop: "ما لا تمنعه هذه الدرجة", nearest: "أقرب شكل قابل للإفراج", expires: "تنتهي",
    uplift: "رفع إلى D2", apply: "تطبيق", recommended: "موصى به", request: "طلب إفراج", purpose: "الغرض (مبررك، يُسجَّل)", sensitiveDeclared: "السمات الحساسة المذكورة في الغرض",
    exemplar: "طلب سجل واحد (نموذج)", records: "السجلات المرشحة", upgrade: "ترقية إلى D3 (غير متزامن)", status: "الحالة", commitment: "الالتزام المختوم",
    queue: "قائمة المراجعة — مجمّعة حسب الخطورة لا حسب الوصول", delta: "ما الذي تغيّر", fullBundle: "عرض الحزمة كاملة", hideBundle: "إخفاء الحزمة الكاملة", noPrior: "لا يوجد إفراج سابق مماثل؛ هذا شكل جديد.",
    accountability: "أنت توقّع بصفتك", retention: "مدة الاحتفاظ", recipient: "المستلم", decide: "قرارك", undecided: "لم يُقرَّر", reject: "رفض — لا يحتاج إلى سبب", approve: "موافقة…", reason: "سببك بكلماتك", confirmApprove: "تأكيد الموافقة على طلب غير روتيني", cancel: "إلغاء",
    sealed: "حكم الآلة مختوم حتى تصوّت.", reveal: "حكم الآلة (يُكشف بعد تصويتك)", agreement: "أنت والآلة متفقان", disagreement: "أنت والآلة مختلفان — كلاهما مسجَّل",
    resolve: "حسم (اكتمل التصويتان)", waiting: "بانتظار المراجع الآخر — تصويته محجوب عنك",
    summary: "أدلة القبول", register: "السجل — كل إفراج وكل رفض", ledger: "الدفتر", bundle: "الحزمة", packRules: "قواعد الحزمة ومصادرها", verifyHint: "تحقّق دون اتصال:",
    quarantined: "محجور — المخرجات لم تطابق؛ لا تُخفَّض أبداً",
  },
} as const;
export type Mc4 = keyof typeof S.en;
export const t = (lang: Uhub, k: Mc4): string => S[lang][k];
