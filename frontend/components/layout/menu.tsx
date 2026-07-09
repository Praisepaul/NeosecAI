import {
  LayoutDashboard,
  Shield,
  Siren,
  Bug,
  Laptop,
  Cloud,
  Fingerprint,
  FileText,
  Bot,
  Settings,
} from "lucide-react";

export const menuItems = [
  {
    title: "Dashboard",
    href: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    title: "Threat Intelligence",
    href: "/threat-intelligence",
    icon: Shield,
  },
  {
    title: "Incidents",
    href: "/incidents",
    icon: Siren,
  },
  {
    title: "Vulnerabilities",
    href: "/vulnerabilities",
    icon: Bug,
  },
  {
    title: "Assets",
    href: "/assets",
    icon: Laptop,
  },
  {
    title: "Cloud",
    href: "/cloud",
    icon: Cloud,
  },
  {
    title: "Identity",
    href: "/identity",
    icon: Fingerprint,
  },
  {
    title: "Reports",
    href: "/reports",
    icon: FileText,
  },
  {
    title: "AI Assistant",
    href: "/ai",
    icon: Bot,
  },
  {
    title: "Settings",
    href: "/settings",
    icon: Settings,
  },
];