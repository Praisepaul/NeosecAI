interface Props {
    severity: string;
}

export default function SeverityBadge({
    severity,
}: Props) {

    const normalized =
        severity.toUpperCase();

    const styles: Record<string, string> = {

        CRITICAL:
            "bg-red-100 text-red-700",

        HIGH:
            "bg-orange-100 text-orange-700",

        MEDIUM:
            "bg-yellow-100 text-yellow-700",

        LOW:
            "bg-green-100 text-green-700",

    };

    return (

        <span
            className={`rounded px-2 py-1 text-xs font-semibold ${
                styles[normalized] ||
                "bg-gray-100 text-gray-700"
            }`}
        >
            {normalized}
        </span>

    );
}