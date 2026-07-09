import { getRelevantThreats } from "@/lib/threatEngine";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function ThreatFeed() {
  const threats = getRelevantThreats();

  return (
    <Card>
      <CardHeader>
        <CardTitle>Relevant Threats</CardTitle>
      </CardHeader>

      <CardContent className="space-y-4">
        {threats.map((threat) => (
          <div key={threat.id} className="border-b pb-3">
            <div className="font-semibold">{threat.title}</div>

            <div className="text-sm text-gray-500">
              {threat.cve} • {threat.severity}
            </div>

            <div className="text-sm">
              {threat.affectedProducts.join(", ")}
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}