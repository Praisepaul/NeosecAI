interface Props {
    search: string;
    severity: string;
    kevOnly: boolean;

    onSearchChange: (
        value: string
    ) => void;

    onSeverityChange: (
        value: string
    ) => void;

    onKevChange: (
        value: boolean
    ) => void;
}

export default function ThreatFilters({
    search,
    severity,
    kevOnly,
    onSearchChange,
    onSeverityChange,
    onKevChange,
}: Props) {

    return (

        <div className="flex flex-col gap-4 rounded-lg border p-4 md:flex-row">

            <input
                type="text"
                placeholder="Search CVE or title..."
                value={search}
                onChange={(event) =>
                    onSearchChange(
                        event.target.value
                    )
                }
                className="rounded-md border px-3 py-2 text-sm md:flex-1"
            />

            <select
                value={severity}
                onChange={(event) =>
                    onSeverityChange(
                        event.target.value
                    )
                }
                className="rounded-md border px-3 py-2 text-sm"
            >

                <option value="">
                    All Severities
                </option>

                <option value="CRITICAL">
                    Critical
                </option>

                <option value="HIGH">
                    High
                </option>

                <option value="MEDIUM">
                    Medium
                </option>

                <option value="LOW">
                    Low
                </option>

            </select>

            <label className="flex items-center gap-2 text-sm">

                <input
                    type="checkbox"
                    checked={kevOnly}
                    onChange={(event) =>
                        onKevChange(
                            event.target.checked
                        )
                    }
                />

                KEV Only

            </label>

        </div>

    );
}