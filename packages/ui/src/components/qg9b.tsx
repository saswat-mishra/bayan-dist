export function EmptyState({ text, testid }: {
    text: string;
    testid?: string;
}) {
    return <div className="empty muted" data-testid={testid ?? "empty"}>{text}</div>;
}
