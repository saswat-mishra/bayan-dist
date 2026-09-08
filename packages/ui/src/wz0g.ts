export type Role = "engineer" | "reviewer" | "lead" | "auditor" | "dba";
export interface Principal {
    id: string;
    displayName: string;
    role: Role;
    lang: string;
    keyType: string;
    authority?: string | null;
    external?: boolean;
    keyName?: string | null;
    publicKey?: string | null;
    custody?: "client" | "gate-colocated";
}
export interface Deployment {
    id: string;
    name: string;
    name_ar?: string;
    pack: string;
    product?: string;
    version?: string;
}
export interface HeadlineJson {
    kind: "releases-now" | "needs-review" | "blocked-fixable" | "blocked-recipient" | "blocked-roster" | "blocked-budget" | "quarantined" | "released" | "refused";
    en: string;
    ar: string;
}
export interface Gate {
    name: string;
    passed: boolean;
    citation: string;
    detail: string;
    remedy_kind: string;
    remedy: string;
    fixable_by_transformation: boolean;
    offending_fields: string[];
}
export interface Blocker {
    level: number;
    field: string;
    field_class: string;
    reason: string;
}
export interface Certificate {
    d: number;
    p: number;
    r: number;
    e: number;
    required_r: number;
    risk_class: string;
    label: string;
    gates: Gate[];
    d_blockers: Blocker[];
    r_notes: string[];
    releasable: boolean;
    disqualified: boolean;
    does_not_stop: string[];
    expires_at: string;
    pack_id: string;
    pack_version: string;
    nearest_releasable: {
        d: number;
        required_r: number;
        dropped: string[];
        load_bearing_lost: string[];
    } | null;
    headline?: HeadlineJson;
    dpe?: string;
    verdict?: string;
    rrsa_class?: string;
    findings?: {
        rule: string;
        target: string;
        action: string;
        detail?: string;
    }[];
}
export interface ManifestField {
    name: string;
    class: string;
    transform: string | null;
    params?: Record<string, unknown>;
    ratified?: boolean;
    loadBearing?: boolean;
}
export interface Recommendation {
    describe: string;
    changes: {
        field: string;
        transform: string;
        params: Record<string, unknown>;
    }[];
    d: string;
    requiredR: string;
    reachesTarget: boolean;
}
export interface Run {
    id: string;
    skill: string;
    version: string;
    status: string;
    params?: Record<string, unknown>;
    lookup?: Lookup | null;
    requester?: string;
    deployment?: string;
    certificate: Certificate;
    certificateMicros: number;
    rows: Record<string, unknown>[];
    outputRef: {
        rows: number;
        digest: string;
    };
    quarantine: {
        rule: string;
        detail: string;
        count: number;
        decertified: boolean;
    } | null;
    manifest: {
        fields: ManifestField[];
    };
    derivedFrom?: string | null;
    transformDigest?: string | null;
    recommendation?: Recommendation | null;
}
export interface UpliftOption {
    describe: string;
    reachesTarget: boolean;
    d: string;
    requiredR: string;
    cost: number;
    loses: string[];
    keeps: string;
    recommended: boolean;
    changes: {
        field: string;
        transform: string;
        params: Record<string, unknown>;
    }[];
}
export interface UpliftMenu {
    target: string;
    current: string;
    asyncRequired: boolean;
    unreachableReason: string | null;
    options: UpliftOption[];
    recommended: string | null;
    recommendation?: Recommendation | null;
}
export interface ReleaseRequest {
    id: string;
    status: string;
    outcome: string;
    certificate: Certificate;
    commitment: string;
    requiredReviews: number;
    releaseId: string | null;
    leafIndex: number | null;
    mechanism: string;
    run?: string | null;
    skill?: string | null;
    purpose?: string;
    lookup?: Lookup | null;
    machineCheck?: {
        verdict: string;
        rrsaClass: string;
    };
    exemplarQuota?: {
        consumed: number;
        limit: number;
    } | null;
    createdAt?: string;
}
export interface WaitingOn {
    kind: string;
    en: string;
    ar: string;
    left?: number;
}
export type OutstandingKind = "eligible" | "waiting";
export interface RequestListItem {
    id: string;
    deployment: string;
    skill: string | null;
    mechanism: string;
    requester: string;
    requesterName?: string;
    purpose: string;
    status: string;
    outcome: string;
    createdAt: string;
    ageSeconds: number;
    requiredReviews: number;
    votes: number;
    headline: HeadlineJson | null;
    waitingOn: WaitingOn;
    outstandingReviewers?: Outstanding[];
    outstandingKind?: OutstandingKind;
    stuck?: boolean;
    stuckAfterSeconds?: number;
    lastReminderAt?: string | null;
    lookup?: Lookup | null;
    releaseId: string | null;
    leafIndex: number | null;
    certificate: string;
}
export interface TimelineStep {
    kind: string;
    done: boolean;
    at: string | null;
    detail: unknown;
    n?: number;
}
export interface Timeline {
    id: string;
    status: string;
    outcome: string;
    headline: HeadlineJson | null;
    steps: TimelineStep[];
    waitingOn: WaitingOn;
    bundle: {
        path: string;
        leafIndex: number;
        verify: string;
        release?: string;
        trustDir?: string;
    } | null;
    suspended: boolean;
    outstandingReviewers?: Outstanding[];
    outstandingKind?: OutstandingKind;
    nextActions?: NextAction[];
}
export interface FeasRow {
    question: string;
    text: string;
    text_ar: string;
    minClass: string;
    minClass_ar?: string;
    minClassWords?: {
        en: string;
        ar: string;
    };
    achievableD: number | null;
    approvalPath: string;
    realTime: boolean | null;
    skills: string[];
    blocked: boolean;
}
export interface CapReason {
    kind: "unratified_field" | "quasi_untransformed" | "direct_untransformed" | "freetext" | "row_level" | "sensitive_undeclared" | "undeclared_field" | "non_exportable";
    field: string | null;
}
export interface Skill {
    name: string;
    version: string;
    riskClass: string;
    maxGradeD: number;
    capReasons?: CapReason[];
    answers: string[];
    description: string;
    description_ar: string;
    params: string[];
    paramExamples: Record<string, string>;
    decertified: boolean;
    certified: boolean;
    certifiedBy?: string | null;
    certifiedAt?: string | null;
    bundleDigest?: string;
}
export interface SkillRequest {
    id: string;
    deployment: string;
    requester: string;
    question: string;
    questionText: string;
    questionText_ar: string;
    fieldsNeeded: string[];
    why: string;
    status: string;
    note: string | null;
    closedBy: string | null;
    closedAt: string | null;
    createdAt: string;
}
export interface Outstanding {
    principal: string;
    displayName: string;
}
export interface Lookup {
    ofRelease: string;
    ofLeaf: number;
    field: string;
    keys: string[];
}
export interface ReceiptHeader {
    request: string;
    requester: {
        principal: string;
        displayName: string;
    };
    purpose: string;
    approvers: {
        principal: string;
        displayName: string;
        role: string;
        authority: string | null;
        verdict: string;
    }[];
    decidedAt: string | null;
    retention: {
        period: string;
        until: string | null;
    };
    disposal: {
        status: "not-released" | "pending" | "attested" | "overdue";
        dueBy: string | null;
        leaf: number | null;
        at?: string | null;
    };
    outcome: string;
    release: string | null;
    leafIndex: number | null;
    lookupAvailable: boolean;
}
export interface RegisterLine {
    line: string;
    lang: {
        en: string;
        ar: string;
    };
    receiptDigest: string;
    leafIndex: number;
    releasedAt: string;
    deployment: string;
    requester: string;
}
export interface NextAction {
    kind: string;
    en: string;
    ar: string;
}
export interface Budget {
    cohort: string;
    period: string;
    consumed: number;
    reserved: number;
    limit: number;
    remaining: number;
    disjoint: boolean;
}
export interface RosterEntry {
    deployment: string;
    principal: string;
    displayName?: string;
    employer: string;
    location: string;
    validFrom: string;
    validUntil: string;
    entryDigest: string;
    clearanceStatus: string | null;
    acknowledgement: {
        digest: string;
        signed: boolean;
    };
    rolledOffAt: string | null;
    destructionAttestation: unknown;
    valid: boolean;
    citizenships?: string[];
    residency?: string[];
    locality?: string;
}
export interface QueueItem {
    id: string;
    deployment: string;
    deploymentName?: string;
    deploymentName_ar?: string;
    skill: string | null;
    mechanism: string;
    riskClass: string;
    requester: string;
    requesterName?: string;
    purpose?: string;
    headline?: HeadlineJson | null;
    ageSeconds?: number;
    lookup?: boolean;
    requiredReviews: number;
    votes: number;
    youVoted: boolean;
    yours: boolean;
    createdAt: string;
}
export interface Brief {
    id: string;
    deployment: string;
    mechanism: string;
    skill: string | null;
    status: string;
    requester: string;
    purpose: string;
    riskClass: string;
    requestDigest: string;
    brief: {
        lang: string;
        direction: "rtl" | "ltr";
        text: string;
        digest: string;
    };
    facts: Record<string, unknown> & {
        below_threshold: number;
        direct_count: number;
        masked_count: number;
        freetext_count: number;
        threshold?: number;
        prior_date?: string | null;
        prior_by?: string | null;
        prior_by_you?: boolean;
        failed_gates?: {
            gate: string;
            detail: string;
            remedy: string;
        }[];
        does_not_stop?: string;
        retention_days?: number;
        retention?: string;
        recipient_org?: string;
        what?: string;
    };
    diff: {
        changed: number | null;
        sameShapeMeans: string;
        comparable?: boolean;
        priorDate?: string | null;
        comparableDefinition?: string;
    };
    certificate: Certificate;
    commitment: string;
    artefact: {
        name: string;
        preview: unknown;
        rows: number;
    };
    fields: ManifestField[];
    requiredReviews: number;
    votes: number;
    yourVote: {
        verdict: string;
        reason: string;
        lang?: string;
        signature?: string;
        public_key_id?: string;
        at_iso?: string;
        presented_digest?: string;
    } | null;
    yours: boolean;
    baseline: {
        tier: number;
        baselineTier: number;
        typedReasonRequired: boolean;
        reasonMinLength: number;
    };
    approveNeedsConfirmation: boolean;
    accountability: {
        reviewer: string;
        retention: string;
        retentionDays?: number;
        retentionText?: string;
        recipient: string;
        recipientOrg?: string;
        recipientEmployer?: string | null;
    };
    recipientEntry?: {
        name: string;
        principal: string;
        rostered: boolean;
        employer?: string;
        location?: string;
        validUntil?: string;
        entryDigest?: string;
    } | null;
    outstandingReviewers?: Outstanding[];
    outstandingKind?: OutstandingKind;
    question?: {
        id: string;
        en: string;
        ar: string;
    } | null;
    createdAt?: string;
    ageSeconds?: number;
    lookup?: Lookup | null;
    certificateDpe?: string;
}
export interface Reveal {
    machineCheck: {
        verdict: string;
        rrsaClass: string;
        findings: {
            rule: string;
            target: string;
            action: string;
            detail?: string;
        }[];
        recommendation?: string;
        recommendationBasis?: string[];
        nonce: string;
        commitment: string;
    };
    commitmentOpens: boolean;
    yourVote: {
        verdict: string;
        reason: string;
    };
    agreement: boolean;
    otherReviews?: {
        reviewer: string;
        name?: string;
        verdict: string;
        reason: string;
    }[];
    status?: string;
    outcome?: string | null;
}
export interface DeploymentStatus {
    id: string;
    pack: {
        id: string;
        version: string;
        digest: string;
        accepted: string;
        pinned: boolean;
        activated: string[];
    };
    suspended: boolean;
    suspension: {
        at: number;
        reason: string;
        leaf: number;
    } | null;
    acceptance: {
        digest: string;
        acceptedBy: string;
        at: string;
        components: string[];
    } | null;
    trustDir?: string;
    outboxDir?: string;
    retention?: {
        vendorDisposal: string;
        clientLogRetention?: string | null;
    };
    primaryFramework?: string | null;
    name?: string;
    nameAr?: string;
}
export interface Summary {
    deployment: string;
    from?: string | null;
    to?: string | null;
    fingerprints: number;
    runs: number;
    released: number;
    refused: number;
    pending?: number;
    pendingVotes?: number;
    autoClearedRunners: number;
    humanReviewed: number;
    votes?: number;
    overrideRate: string;
    agreementRate: string;
    agreementText?: {
        en: string;
        ar: string;
    };
    overrideText?: {
        en: string;
        ar: string;
    };
    byGrade: Record<string, number>;
    budget: Budget[];
}
export interface RegisterRow {
    id: string;
    deployment: string;
    skill: string | null;
    mechanism: string;
    requester: string;
    purpose?: string;
    status: string;
    outcome: string;
    release: string | null;
    leafIndex: number | null;
    certificate: string;
    disqualified: boolean;
    failedGates: string[];
    reviews: {
        reviewer: string;
        verdict: string;
    }[];
    createdAt: string;
    headline: HeadlineJson | null;
    outbox: string | null;
    header?: ReceiptHeader | null;
}
export interface LedgerEntry {
    index: number;
    leafHash: string;
    type: string;
    outcome?: string;
    rrsaClass?: string;
    humanReviews?: string[];
    request?: string | null;
    release?: string | null;
    principal?: string;
    keyName?: string;
    pack?: string;
    hour?: string;
    reason?: string;
    by?: string;
    at?: string;
}
export interface Ledger {
    origin: string;
    size: number;
    checkpoint: string | null;
    integrity: string[];
    entries: LedgerEntry[];
}
export interface BundleFiles {
    release: string;
    path: string;
    files: Record<string, {
        bytes: number;
        sha256: string;
        text: string | null;
    }>;
    header?: ReceiptHeader | null;
    trustDir?: string;
    verify?: string;
    registerLine?: RegisterLine | null;
}
export interface ControlRow {
    control: string;
    title: string | null;
    evidence: string | null;
    releases: number;
    refusals: number;
    sensorHours: number;
    lastEvidenceAt?: string | null;
}
export interface Gap {
    control: string;
    why: "no-refusal" | "no-release" | "sensor-absent" | "no-sensor-hour";
    sensorPresent: boolean;
}
export interface ControlsIndex {
    deployment: string;
    period: string | null;
    pack: {
        id: string;
        version: string;
        digest: string;
    };
    primaryFramework?: string | null;
    frameworkTitles?: Record<string, {
        en: string;
        ar: string;
    }>;
    sensorHours: number;
    sensorPresent?: boolean;
    frameworks: Record<string, ControlRow[]>;
    gaps?: Record<string, Gap[]>;
}
export interface LedgerRange {
    deployment: string;
    from: string | null;
    to: string | null;
    periods: string[];
    leaves: number;
}
export interface EvidenceHit {
    leaf: number;
    outcome: string;
    decidedAt: string;
    request: string | null;
    release: string | null;
    headline: HeadlineJson;
    mechanisms: string[];
    label: string;
    header?: ReceiptHeader | null;
}
export interface ControlEvidence {
    deployment: string;
    framework: string;
    control: string;
    period: string | null;
    provenance: Record<string, string> | null;
    evidence: EvidenceHit[];
}
export interface EvidencePack {
    deployment: string;
    period: string;
    builtAt?: number;
    manifestDigest: string;
    fromSize: number;
    toSize: number;
    flags: {
        zeroRefusals: boolean;
        zeroSensorEvents: boolean;
        sensorAbsent: boolean;
        attention?: string | null;
    };
    path: string;
    files?: string[];
}
export interface SensorHour {
    hour: string;
    events: number;
    byClass: Record<string, number>;
    root: string;
    leafIndex: number | null;
    sealed: boolean;
}
export interface Enrolment {
    principal: string;
    keyName: string;
    publicKey: string;
    genesis: boolean;
    requestedAt: string;
    approvedBy: string | null;
    approvedAt: string | null;
    leafIndex: number | null;
    status: string;
}
export interface Acceptance {
    deployment: string;
    accepted: Record<string, unknown> | null;
    draft: {
        digest: string;
        pack: {
            id: string;
            version: string;
            digest: string;
        };
        skills: {
            name: string;
            version: string;
        }[];
    };
    current: {
        digest: string;
    };
    delta?: string[];
}
export interface FieldClass {
    deployment: string;
    field: string;
    class: string;
    proposedBy: string;
    ratifiedBy: string | null;
    ratifiedByName?: string | null;
    ratifiedAt: string | null;
    ratified: boolean;
    signature: string | null;
    guidance: Record<string, unknown>;
    impact: {
        skills: string[];
        cappedAtD1: string[];
        text: string;
        text_ar?: string;
    };
}
export interface Pack {
    id: string;
    version: string;
    digest: string;
    name?: string;
    name_ar?: string;
    rules: {
        id: string;
        citation: string;
        quote: string;
        evidence: string;
        advisory?: boolean;
        note?: string;
    }[];
    fieldDefaults: Record<string, {
        class: string;
    }>;
    review?: Record<string, unknown> & {
        roleFloors?: Record<string, number>;
        stuckAfterSeconds?: number;
        threshold?: number;
    };
    budget?: {
        perCohortLimit?: number;
        period?: string;
        exemplarQuota?: number;
    };
    retention?: {
        vendorDisposal?: string;
        clientLogRetention?: string;
    };
    lookup?: {
        maxKeys: number;
    };
    terms?: Record<string, Record<string, {
        label: string;
        line: string;
    }>>;
    primaryFramework?: string;
    doesNotStopExample?: {
        en: string;
        ar: string;
    };
}
