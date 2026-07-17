"use client";

import { Threat } from "@/types/threat";
import SeverityBadge from "./SeverityBadge";

interface Props {
    threats: Threat[];
}

export default function ThreatTable({
    threats,
}: Props) {

    return (

        <div className="overflow-x-auto rounded-lg border">

            <table className="w-full text-sm">

                <thead className="border-b bg-muted/50">

                    <tr>

                        <th className="px-4 py-3 text-left">
                            CVE
                        </th>

                        <th className="px-4 py-3 text-left">
                            Severity
                        </th>

                        <th className="px-4 py-3 text-left">
                            CVSS
                        </th>

                        <th className="px-4 py-3 text-left">
                            Risk
                        </th>

                        <th className="px-4 py-3 text-left">
                            EPSS
                        </th>

                        <th className="px-4 py-3 text-left">
                            KEV
                        </th>

                        <th className="px-4 py-3 text-left">
                            Assets
                        </th>

                    </tr>

                </thead>

                <tbody>

                    {threats.map((threat) => (

                        <tr
                            key={threat.cve}
                            className="border-b last:border-0 hover:bg-muted/30"
                        >

                            <td className="px-4 py-4">

                                <div className="font-semibold">
                                    {threat.cve}
                                </div>

                                <div className="mt-1 max-w-md truncate text-xs text-muted-foreground">
                                    {threat.title}
                                </div>

                            </td>

                            <td className="px-4 py-4">

                                <SeverityBadge
                                    severity={
                                        threat.cvss?.severity ||
                                        "UNKNOWN"
                                    }
                                />

                            </td>

                            <td className="px-4 py-4">

                                {threat.cvss?.score ??
                                    "N/A"}

                            </td>

                            <td className="px-4 py-4 font-semibold">

                                {threat.risk_score}

                            </td>

                            <td className="px-4 py-4">

                                {threat.epss
                                    ? (
                                        threat.epss.score *
                                        100
                                    ).toFixed(2) + "%"
                                    : "N/A"}

                            </td>

                            <td className="px-4 py-4">

                                {threat.kev
                                    ? "Yes"
                                    : "No"}

                            </td>

                            <td className="px-4 py-4">

                                {threat.matched_assets
                                    ?.length || 0}

                            </td>

                        </tr>

                    ))}

                </tbody>

            </table>

            {threats.length === 0 && (

                <div className="p-8 text-center text-muted-foreground">

                    No threats found.

                </div>

            )}

        </div>

    );
}