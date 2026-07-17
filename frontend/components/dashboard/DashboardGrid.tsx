interface Props {
    children: React.ReactNode;
}

export default function DashboardGrid({
    children,
}: Props) {
    return (
        <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">
            {children}
        </div>
    );
}