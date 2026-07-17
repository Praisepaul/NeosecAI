import { Badge } from "@/components/ui/badge";


interface Props {

    severity: string | null;

}


export default function SeverityBadge({
    severity,
}: Props) {

    const value =
        severity?.toUpperCase() || "UNKNOWN";


    const styles: Record<
        string,
        string
    > = {

        CRITICAL:
            "bg-red-600 text-white",

        HIGH:
            "bg-orange-500 text-white",

        MEDIUM:
            "bg-yellow-500 text-black",

        LOW:
            "bg-green-600 text-white",

        UNKNOWN:
            "bg-muted text-muted-foreground",

    };


    return (

        <Badge
            className={
                styles[value] ||
                styles.UNKNOWN
            }
        >

            {value}

        </Badge>

    );

}