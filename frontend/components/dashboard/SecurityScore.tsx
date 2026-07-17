import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";

interface Props {
    score: number;
}

export default function SecurityScore({
    score,
}: Props) {
    return (
        <Card>
            <CardHeader>
                <CardTitle>Security Score</CardTitle>
            </CardHeader>

            <CardContent>
                <div className="text-5xl font-bold">
                    {score}
                </div>

                <p className="mt-2 text-sm text-muted-foreground">
                    Overall security posture
                </p>
            </CardContent>
        </Card>
    );
}