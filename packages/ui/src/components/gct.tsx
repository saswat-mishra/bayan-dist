import type { ReactNode } from "react";
export function Page({ title, intro, testid, className, children }: {
    title: ReactNode;
    intro?: ReactNode;
    testid?: string;
    className?: string;
    children?: ReactNode;
}) {
    return (<div className={["page", className].filter(Boolean).join(" ")} data-testid={testid}>
      <div className="page-head">
        <h1 data-testid="page-title">{title}</h1>
        {intro && <p className="page-intro" data-testid="page-intro">{intro}</p>}
      </div>
      {children}
    </div>);
}
export function Section({ heading, purpose, testid, className, aside, children }: {
    heading: ReactNode;
    purpose?: ReactNode;
    testid?: string;
    className?: string;
    aside?: ReactNode;
    children?: ReactNode;
}) {
    return (<section className={["card", className].filter(Boolean).join(" ")} data-testid={testid}>
      <div className="section-head"><h2>{heading}</h2>{aside}</div>
      {purpose && <p className="section-purpose" data-testid="section-purpose">{purpose}</p>}
      {children}
    </section>);
}
