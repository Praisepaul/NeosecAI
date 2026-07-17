"use client";

import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
} from "recharts";

interface Vendor {
    vendor: string;
    count: number;
}

interface Props {
    vendors: Vendor[];
}

export default function VendorChart({
    vendors,
}: Props) {
    return (
        <ResponsiveContainer
            width="100%"
            height={300}
        >
            <BarChart
                data={vendors}
                layout="vertical"
                margin={{
                    left: 30,
                    right: 20,
                }}
            >
                <XAxis
                    type="number"
                />

                <YAxis
                    type="category"
                    dataKey="vendor"
                    width={100}
                    tick={{ fontSize: 11 }}
                />

                <Tooltip />

                <Bar
                    dataKey="count"
                    name="Threats"
                />
            </BarChart>
        </ResponsiveContainer>
    );
}