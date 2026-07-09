export interface Threat {
  id: string;
  title: string;
  source: string;
  severity: "Critical" | "High" | "Medium" | "Low";
  cve?: string;
  affectedProducts: string[];
  published: string;
  summary: string;
  exploited: boolean;
}