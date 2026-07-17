import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";

import { RecentThreat } from "@/types/dashboard";

interface Props {
    threats: RecentThreat[];
}

export default function ThreatFeed({
    threats,
}: Props) {
    return (
        <Card>
            <CardHeader>
                <CardTitle>Recent Threats</CardTitle>
            </CardHeader>

            <CardContent className="space-y-4">

                {threats.map((threat) => (
                    <div
                        key={threat.cve}
                        className="border-b pb-4 last:border-0"
                    >
                        <div className="flex items-start justify-between gap-4">

                            <div className="min-w-0">

                                <div className="font-semibold">
                                    {threat.cve}
                                </div>

                                <div className="mt-1 text-sm text-muted-foreground">
                                    {threat.title}
                                </div>

                            </div>

                            <div className="shrink-0 text-right">

                                <div className="text-sm font-semibold">
                                    Risk {threat.risk_score}
                                </div>

                                <div className="text-xs text-muted-foreground">
                                    CVSS {threat.cvss.score}
                                </div>

                            </div>

                        </div>
                    </div>
                ))}

            </CardContent>
        </Card>
    );
}