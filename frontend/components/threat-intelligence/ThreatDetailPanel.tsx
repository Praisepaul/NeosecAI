"use client";

import { X } from "lucide-react";

import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";

import { Button } from "@/components/ui/button";

import { Threat } from "@/types/threat";

interface Props {
    threat: Threat;
    onClose: () => void;
}

export default function ThreatDetailPanel({
    threat,
    onClose,
}: Props) {
    return (
        <aside className="w-full h-full bg-background">

            <div className="flex h-full flex-col">

                {/* Header */}
                <div className="flex items-center justify-between border-b p-4">

                    <div>
                        <h2 className="font-semibold">
                            Threat Details
                        </h2>

                        <p className="text-sm text-muted-foreground">
                            {threat.cve}
                        </p>
                    </div>

                    <Button
                        variant="ghost"
                        size="icon"
                        onClick={onClose}
                    >
                        <X className="h-4 w-4" />
                    </Button>

                </div>

                {/* Scrollable Details */}
                <div className="flex-1 overflow-y-auto p-4 space-y-4">

                    <Card>
                        <CardHeader>
                            <CardTitle>
                                {threat.title}
                            </CardTitle>
                        </CardHeader>

                        <CardContent className="space-y-3">

                            <div>
                                <p className="text-sm text-muted-foreground">
                                    Description
                                </p>

                                <p className="text-sm">
                                    {threat.description ||
                                        "No description available."}
                                </p>
                            </div>

                            <div>
                                <p className="text-sm text-muted-foreground">
                                    Risk Score
                                </p>

                                <p className="font-semibold">
                                    {threat.risk_score}
                                </p>
                            </div>

                            <div>
                                <p className="text-sm text-muted-foreground">
                                    CVSS
                                </p>

                                <p>
                                    {threat.cvss?.score ?? "N/A"}
                                </p>
                            </div>

                            <div>
                                <p className="text-sm text-muted-foreground">
                                    Severity
                                </p>

                                <p>
                                    {threat.cvss?.severity || "UNKNOWN"}
                                </p>
                            </div>

                        </CardContent>
                    </Card>

                    {/* Technology */}
                    <Card>
                        <CardHeader>
                            <CardTitle>
                                Technology
                            </CardTitle>
                        </CardHeader>

                        <CardContent className="space-y-3">

                            <div>
                                <p className="text-sm text-muted-foreground">
                                    Vendors
                                </p>

                                <p className="text-sm">
                                    {threat.technology?.vendors?.join(", ") ||
                                        "None"}
                                </p>
                            </div>

                            <div>
                                <p className="text-sm text-muted-foreground">
                                    Products
                                </p>

                                <p className="text-sm">
                                    {threat.technology?.products?.join(", ") ||
                                        "None"}
                                </p>
                            </div>

                            <div>
                                <p className="text-sm text-muted-foreground">
                                    Versions
                                </p>

                                <p className="text-sm">
                                    {threat.technology?.versions?.join(", ") ||
                                        "None"}
                                </p>
                            </div>

                        </CardContent>
                    </Card>

                    {/* References */}
                    <Card>
                        <CardHeader>
                            <CardTitle>
                                References
                            </CardTitle>
                        </CardHeader>

                        <CardContent className="space-y-2">

                            {threat.references?.length ? (

                                threat.references.map((reference) => (

                                    <a
                                        key={reference}
                                        href={reference}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="block break-all text-sm text-blue-500 hover:underline"
                                    >
                                        {reference}
                                    </a>

                                ))

                            ) : (

                                <p className="text-sm text-muted-foreground">
                                    No references available.
                                </p>

                            )}

                        </CardContent>
                    </Card>

                    {/* Sources */}
                    <Card>
                        <CardHeader>
                            <CardTitle>
                                Sources
                            </CardTitle>
                        </CardHeader>

                        <CardContent className="space-y-2">

                            <p className="text-sm">
                                NVD:{" "}
                                {threat.sources?.nvd
                                    ? "Available"
                                    : "Not available"}
                            </p>

                            <p className="text-sm">
                                GitHub:{" "}
                                {threat.sources?.github
                                    ? "Available"
                                    : "Not available"}
                            </p>

                            <p className="text-sm">
                                CISA:{" "}
                                {threat.sources?.cisa
                                    ? "Available"
                                    : "Not available"}
                            </p>

                            <p className="text-sm">
                                EPSS:{" "}
                                {threat.sources?.epss
                                    ? "Available"
                                    : "Not available"}
                            </p>

                        </CardContent>
                    </Card>

                </div>

            </div>

        </aside>
    );
}