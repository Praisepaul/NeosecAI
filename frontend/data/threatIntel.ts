import { Threat } from "@/types/threat";

export const threatFeed: Threat[] = [
  {
    id: "1",
    title: "Critical Grafana Authentication Bypass",
    source: "Grafana Security Advisory",
    severity: "Critical",
    cve: "CVE-2026-11111",
    affectedProducts: ["Grafana"],
    published: "2026-07-07",
    exploited: true,
    summary:
      "Authentication bypass vulnerability affecting Grafana instances.",
  },

  {
    id: "2",
    title: "OpenSearch Remote Code Execution",
    source: "NVD",
    severity: "High",
    cve: "CVE-2026-22222",
    affectedProducts: ["OpenSearch"],
    published: "2026-07-06",
    exploited: false,
    summary:
      "Remote code execution vulnerability discovered in OpenSearch.",
  },

  {
    id: "3",
    title: "Windows Print Spooler",
    source: "Microsoft",
    severity: "Medium",
    cve: "CVE-2026-33333",
    affectedProducts: ["Windows Server"],
    published: "2026-07-04",
    exploited: false,
    summary:
      "Privilege escalation vulnerability affecting Print Spooler.",
  },

  {
    id: "4",
    title: "WordPress Plugin Vulnerability",
    source: "NVD",
    severity: "Critical",
    cve: "CVE-2026-44444",
    affectedProducts: ["WordPress"],
    published: "2026-07-05",
    exploited: true,
    summary:
      "Critical plugin vulnerability.",
  },
];