"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { menuItems } from "./menu";

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-54 min-w-54 shrink-0 border-r min-h-screen">
      <div className="text-2xl font-bold p-6">NeoSOC AI</div>

      <nav className="px-3 space-y-1">
        {menuItems.map((item) => {
          const Icon = item.icon;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 rounded-lg px-4 py-3 transition ${
                pathname === item.href
                  ? "bg-primary text-primary-foreground"
                  : "hover:bg-muted"
              }`}
            >
              <Icon size={18} />
              {item.title}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}