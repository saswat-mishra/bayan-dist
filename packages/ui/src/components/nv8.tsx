export function Progress({ label, testid }: {
    label: string;
    testid?: string;
}) {
    return (<div className="progress" role="status" aria-live="polite" data-testid={testid ?? "progress"}>
      <span className="spinner" aria-hidden="true"/>
      <span>{label}</span>
    </div>);
}
