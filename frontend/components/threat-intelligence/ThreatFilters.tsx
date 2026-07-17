"use client";


import {
    Input,
} from "@/components/ui/input";


import {
    Button,
} from "@/components/ui/button";


import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";


import {
    Search,
    RotateCcw,
} from "lucide-react";


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

    onReset: () => void;

}


export default function ThreatFilters({

    search,

    severity,

    kevOnly,

    onSearchChange,

    onSeverityChange,

    onKevChange,

    onReset,

}: Props) {


    function resetFilters() {

        onReset();

    }


    return (

        <div className="flex flex-col gap-3 rounded-lg border bg-card p-4 lg:flex-row lg:items-center">

            <div className="relative flex-1">

                <Search
                    className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground"
                />


                <Input

                    value={search}

                    onChange={(event) =>
                        onSearchChange(
                            event.target.value
                        )
                    }

                    placeholder="Search CVE, title, product, vendor..."

                    className="pl-9"

                />

            </div>


            <Select
    value={severity}
    onValueChange={(value) => {
        if (value) {
            onSeverityChange(value);
        }
    }}
>
    <SelectTrigger className="w-full lg:w-[160px]">
        <SelectValue placeholder="Severity" />
    </SelectTrigger>

    <SelectContent>

        <SelectItem value="ALL">
            All Severities
        </SelectItem>

        <SelectItem value="CRITICAL">
            Critical
        </SelectItem>

        <SelectItem value="HIGH">
            High
        </SelectItem>

        <SelectItem value="MEDIUM">
            Medium
        </SelectItem>

        <SelectItem value="LOW">
            Low
        </SelectItem>

    </SelectContent>
</Select>


            <Button

                variant={
                    kevOnly
                        ? "default"
                        : "outline"
                }

                onClick={() =>
                    onKevChange(!kevOnly)
                }

            >

                KEV Only

            </Button>


            <Button

                variant="ghost"

                size="icon"

                onClick={resetFilters}

            >

                <RotateCcw
                    className="h-4 w-4"
                />

            </Button>

        </div>

    );

}