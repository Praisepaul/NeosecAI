"use client";

import {
    PieChart,
    Pie,
    Tooltip,
    Cell,
    ResponsiveContainer,
    Legend,
} from "recharts";

interface SeverityData {
    critical: number;
    high: number;
    medium: number;
    low: number;
}

interface Props {
    data: SeverityData;
}

const COLORS = [
    "#ef4444",
    "#fb923c",
    "#eab308",
    "#22c55e",
];

export default function SeverityChart({
    data,
}: Props) {
    const chart = [
        {
            name: "Critical",
            value: data.critical,
        },
        {
            name: "High",
            value: data.high,
        },
        {
            name: "Medium",
            value: data.medium,
        },
        {
            name: "Low",
            value: data.low,
        },
    ];

    return (
        <ResponsiveContainer
            width="100%"
            height={300}
        >
            <PieChart>
                <Pie
                    data={chart}
                    dataKey="value"
                    nameKey="name"
                    outerRadius={110}
                    label
                >
                    {chart.map((_, index) => (
                        <Cell
                            key={`cell-${index}`}
                            fill={COLORS[index]}
                        />
                    ))}
                </Pie>

                <Tooltip />

                <Legend />
            </PieChart>
        </ResponsiveContainer>
    );
}