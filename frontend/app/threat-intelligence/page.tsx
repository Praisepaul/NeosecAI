"use client";

import { useMemo, useState } from "react";

import ThreatFilters
    from "@/components/threat-intelligence/ThreatFilters";

import ThreatTable
    from "@/components/threat-intelligence/ThreatTable";

import { useThreats }
    from "@/src/hooks/useThreats";

export default function ThreatIntelPage() {

    const {
        threats,
        loading,
        error,
    } = useThreats();

    const [search, setSearch] =
        useState("");

    const [severity, setSeverity] =
        useState("");

    const [kevOnly, setKevOnly] =
        useState(false);

    const filteredThreats =
        useMemo(() => {

            return threats.filter(
                (threat) => {

                    const searchValue =
                        search.toLowerCase();

                    const matchesSearch =
                        threat.cve
                            .toLowerCase()
                            .includes(searchValue) ||

                        (
                            threat.title ||
                            ""
                        )
                            .toLowerCase()
                            .includes(searchValue);

                    const matchesSeverity =
                        !severity ||
                        threat.cvss?.severity ===
                        severity;

                    const matchesKev =
                        !kevOnly ||
                        threat.kev;

                    return (
                        matchesSearch &&
                        matchesSeverity &&
                        matchesKev
                    );

                }
            );

        }, [
            threats,
            search,
            severity,
            kevOnly,
        ]);

    if (loading) {

        return (

            <div className="p-6">

                Loading threat intelligence...

            </div>

        );

    }

    if (error) {

        return (

            <div className="p-6 text-red-500">

                {error}

            </div>

        );

    }

    return (

        <div className="space-y-6">

            <div>

                <h1 className="text-3xl font-bold">

                    Threat Intelligence

                </h1>

                <p className="text-muted-foreground">

                    Monitor vulnerabilities and security threats affecting your environment.

                </p>

            </div>

            <ThreatFilters

                search={search}

                severity={severity}

                kevOnly={kevOnly}

                onSearchChange={setSearch}

                onSeverityChange={setSeverity}

                onKevChange={setKevOnly}

            />

            <div className="text-sm text-muted-foreground">

                Showing{" "}

                <span className="font-semibold">

                    {filteredThreats.length}

                </span>{" "}

                of{" "}

                <span className="font-semibold">

                    {threats.length}

                </span>{" "}

                threats

            </div>

            <ThreatTable
                threats={filteredThreats}
            />

        </div>

    );

}