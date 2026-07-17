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

const COLORS = ["#ef4444", "#fb923c", "#eab308", "#22c55e"];

export default function SeverityChart({ data }: Props) {
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
    <div className="h-[320px] w-full min-w-0">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={chart}
            dataKey="value"
            nameKey="name"
            // Responsive size
            outerRadius="65%"
            // Keep the pie centered
            cx="50%"
            cy="45%"
            label
          >
            {chart.map((_, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index]} />
            ))}
          </Pie>

          <Tooltip />

          <Legend verticalAlign="bottom" height={36} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
