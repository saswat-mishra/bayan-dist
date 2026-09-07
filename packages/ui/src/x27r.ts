import { ApiError } from './vhq7';
import type { Lang } from './gna';
interface Rule {
    match: (status: number, text: string) => boolean;
    en: string;
    ar: string;
}
const RULES: Rule[] = [
    { match: (s, t) => s === 423 || /suspended/.test(t), en: "This deployment is suspended after a sensor event. A principal with authority must clear it before anything can leave.", ar: "هذا النشر موقوف بعد حدث من المستشعر. يجب أن ترفع جهة ذات صلاحية الإيقاف قبل أن يخرج أي شيء." },
    { match: (_s, t) => /roster entry missing or expired/.test(t), en: "Your roster entry is missing or has expired — ask your delivery lead to renew it.", ar: "قيدك في سجل التكليف مفقود أو منتهٍ — اطلب من قائد التسليم تجديده." },
    { match: (_s, t) => /own request/.test(t), en: "You requested this release, so you cannot review it. Another reviewer must.", ar: "أنت من طلب هذا الإفراج، لذا لا يمكنك مراجعته. يجب أن يراجعه مراجع آخر." },
    { match: (_s, t) => /already voted/.test(t), en: "Your vote on this request is already recorded.", ar: "تصويتك على هذا الطلب مسجَّل مسبقاً." },
    { match: (_s, t) => /reason/.test(t) && /(short|required|characters|typed)/.test(t), en: "Approving above the baseline needs your reason, in your own words (at least 20 characters).", ar: "الموافقة فوق الحد الأساسي تحتاج إلى سببك بكلماتك (20 حرفاً على الأقل)." },
    { match: (_s, t) => /presented digest|what was shown/.test(t) && !/signature/.test(t), en: "The brief changed while you were reading it. Reload and read it again before deciding.", ar: "تغيّر الملخّص أثناء قراءتك. أعد التحميل واقرأه مرة أخرى قبل أن تقرّر." },
    { match: (_s, t) => /no enrolled key|enrol one/.test(t), en: "This browser holds no enrolled key. Enrol it from the header and ask another authority to approve.", ar: "لا يحمل هذا المتصفح مفتاحاً معتمداً. سجّله من الترويسة واطلب من جهة أخرى اعتماده." },
    { match: (_s, t) => /signature does not verify|not this reviewer's enrolled key/.test(t), en: "Your signature did not verify against your enrolled key. Re-enrol this browser's key and try again.", ar: "لم يُتحقق من توقيعك مقابل مفتاحك المعتمد. أعد تسجيل مفتاح هذا المتصفح وحاول مرة أخرى." },
    { match: (_s, t) => /ten minutes|clock/.test(t), en: "Your device clock is more than ten minutes from the gate's. Fix the clock and sign again.", ar: "ساعة جهازك تبعد أكثر من عشر دقائق عن ساعة البوابة. اضبط الساعة ووقّع مرة أخرى." },
    { match: (_s, t) => /budget|quota/.test(t), en: "The period budget for this cohort is exhausted. Wait for the next period or ask your delivery lead.", ar: "ميزانية الفترة لهذه المجموعة مستنفدة. انتظر الفترة التالية أو اسأل قائد التسليم." },
    { match: (_s, t) => /authority/.test(t), en: "This action needs a principal with authority under the client's control framework.", ar: "يحتاج هذا الإجراء إلى جهة ذات صلاحية بموجب إطار الضوابط لدى العميل." },
    { match: (_s, t) => /already ratified/.test(t), en: "This field class is already ratified.", ar: "فئة هذا الحقل مصدَّقة مسبقاً." },
    { match: (_s, t) => /already enrolled|awaiting approval/.test(t), en: "A key for this reviewer is already enrolled or awaiting approval.", ar: "مفتاح هذا المراجع مسجَّل مسبقاً أو بانتظار الاعتماد." },
    { match: (_s, t) => /pack .*digest|pack upgrade|accepted digest/.test(t), en: "The policy pack on disk differs from the accepted one. An authority must approve the upgrade first.", ar: "حزمة السياسات على القرص تختلف عن المعتمدة. يجب أن تعتمد جهة ذات صلاحية الترقية أولاً." },
    { match: (_s, t) => /not suspended/.test(t), en: "This deployment is not suspended.", ar: "هذا النشر ليس موقوفاً." },
    { match: (_s, t) => /decertified|quarantin/.test(t), en: "This skill was quarantined: its output did not conform. It cannot run until it is re-certified.", ar: "هذه المهارة محجورة: مخرجاتها لم تطابق. لا يمكن تشغيلها حتى يُعاد اعتمادها." },
    { match: (s) => s === 403, en: "Your role may not do this.", ar: "دورك لا يسمح بهذا الإجراء." },
    { match: (s) => s === 404, en: "That no longer exists — it may have been resolved or rolled off. Reload the list.", ar: "لم يعد هذا موجوداً — ربما حُسم أو أُزيل. أعد تحميل القائمة." },
    { match: (s) => s === 409, en: "The gate refused because the state has moved on. Reload and look again.", ar: "رفضت البوابة لأن الحالة تغيّرت. أعد التحميل وانظر مرة أخرى." },
    { match: (s) => s === 422, en: "Something in the form is not acceptable to the gate. Check the fields and try again.", ar: "شيء في النموذج غير مقبول لدى البوابة. تحقّق من الحقول وحاول مرة أخرى." },
];
export function explain(e: unknown, lang: Lang): string {
    if (e instanceof ApiError) {
        const text = String(e.body.error ?? e.body.detail ?? "");
        const rule = RULES.find((r) => r.match(e.status, text));
        if (rule)
            return rule[lang];
        return lang === "ar" ? `رفضت البوابة الطلب (${e.status}). ${text}` : `The gate refused (${e.status}). ${text}`;
    }
    if (e instanceof TypeError)
        return lang === "ar" ? "تعذّر الوصول إلى البوابة. هل تعمل على هذا الجهاز؟" : "The gate could not be reached. Is it running on this machine?";
    return lang === "ar" ? "حدث خطأ غير متوقع." : "Something unexpected went wrong.";
}
