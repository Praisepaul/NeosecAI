import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";

interface MetricCardProps {
    title: string;
    value: string | number;
    description?: string;
}

export default function MetricCard({
    title,
    value,
    description,
}: MetricCardProps) {
    return (
        <Card>
            <CardHeader>
                <CardTitle className="text-sm font-medium">
                    {title}
                </CardTitle>
            </CardHeader>

            <CardContent>
                <div className="text-3xl font-bold">
                    {value}
                </div>

                {description && (
                    <p className="mt-1 text-sm text-muted-foreground">
                        {description}
                    </p>
                )}
            </CardContent>
        </Card>
    );
}