"use client";

import { useEffect, useMemo, useState } from "react";

import ThreatFilters from "@/components/threat-intelligence/ThreatFilters";
import ThreatTable from "@/components/threat-intelligence/ThreatTable";
import ThreatDetailPanel from "@/components/threat-intelligence/ThreatDetailPanel";
import AppErrorState from "@/components/errors/AppErrorState";

import { Threat } from "@/types/threat";

export default function ThreatIntelPage() {
  const [threats, setThreats] = useState<Threat[]>([]);
  const [loading, setLoading] = useState(true);
  const [errorType, setErrorType] = useState<
    "network" | "api" | "unknown" | null
  >(null);

  const [kevOnly, setKevOnly] = useState(false);
  const [search, setSearch] = useState("");
  const [severity, setSeverity] = useState("ALL");

  const [selectedThreat, setSelectedThreat] = useState<Threat | null>(null);

  /*
    |--------------------------------------------------------------------------
    | Sorting
    |--------------------------------------------------------------------------
    */

  const [sortColumn, setSortColumn] = useState("severity");

  const [sortDirection, setSortDirection] = useState<"asc" | "desc">("desc");

  /*
    |--------------------------------------------------------------------------
    | Pagination
    |--------------------------------------------------------------------------
    */

  const [currentPage, setCurrentPage] = useState(1);

  const rowsPerPage = 10;

  /*
    |--------------------------------------------------------------------------
    | Fetch threats
    |--------------------------------------------------------------------------
    */

  useEffect(() => {
    async function fetchThreats() {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/threats/");

        if (!response.ok) {
          setErrorType("api");
          return;
        }

        const data = await response.json();

        setThreats(data);
      } catch (error) {
        if (error instanceof TypeError && error.message === "Failed to fetch") {
          setErrorType("network");
        } else {
          setErrorType("unknown");
        }
      } finally {
        setLoading(false);
      }
    }

    fetchThreats();
  }, []);

  /*
    |--------------------------------------------------------------------------
    | FILTERING
    |--------------------------------------------------------------------------
    */

  const filteredThreats = useMemo(() => {
    return threats.filter((threat) => {
      const searchValue = search.toLowerCase();

      const matchesSearch =
        threat.cve.toLowerCase().includes(searchValue) ||
        threat.title?.toLowerCase().includes(searchValue) ||
        threat.technology?.products?.some((product) =>
          product.toLowerCase().includes(searchValue),
        ) ||
        threat.technology?.vendors?.some((vendor) =>
          vendor.toLowerCase().includes(searchValue),
        );

      const matchesSeverity =
        severity === "ALL" || threat.cvss?.severity === severity;

      const matchesKev = !kevOnly || threat.kev === true;

      return matchesSearch && matchesSeverity && matchesKev;
    });
  }, [threats, search, severity, kevOnly]);

  /*
    |--------------------------------------------------------------------------
    | SORTING
    |--------------------------------------------------------------------------
    */

  const sortedThreats = useMemo(() => {
    const sorted = [...filteredThreats];

    const severityOrder: Record<string, number> = {
      CRITICAL: 5,
      HIGH: 4,
      MEDIUM: 3,
      LOW: 2,
      UNKNOWN: 1,
    };

    sorted.sort((a, b) => {
      let valueA: string | number;
      let valueB: string | number;

      switch (sortColumn) {
        case "cve":
          valueA = a.cve;
          valueB = b.cve;

          break;

        case "title":
          valueA = a.title || "";
          valueB = b.title || "";

          break;

        case "severity":
          valueA = severityOrder[a.cvss?.severity || "UNKNOWN"] || 0;

          valueB = severityOrder[b.cvss?.severity || "UNKNOWN"] || 0;

          break;

        case "cvss":
          valueA = a.cvss?.score ?? -1;

          valueB = b.cvss?.score ?? -1;

          break;

        case "risk":
          valueA = a.risk_score ?? 0;

          valueB = b.risk_score ?? 0;

          break;

        case "epss":
          valueA = a.epss?.score ?? -1;

          valueB = b.epss?.score ?? -1;

          break;

        case "assets":
          valueA = a.matched_assets?.length ?? 0;

          valueB = b.matched_assets?.length ?? 0;

          break;

        case "published":
          valueA = a.published ? new Date(a.published).getTime() : 0;

          valueB = b.published ? new Date(b.published).getTime() : 0;

          break;

        default:
          valueA = 0;
          valueB = 0;
      }

      let result: number;

      if (typeof valueA === "string" && typeof valueB === "string") {
        result = valueA.localeCompare(valueB);
      } else {
        result = Number(valueA) - Number(valueB);
      }

      return sortDirection === "asc" ? result : -result;
    });

    return sorted;
  }, [filteredThreats, sortColumn, sortDirection]);

  /*
    |--------------------------------------------------------------------------
    | PAGINATION
    |--------------------------------------------------------------------------
    */

  const totalPages = Math.ceil(sortedThreats.length / rowsPerPage);

  const paginatedThreats = useMemo(() => {
    const startIndex = (currentPage - 1) * rowsPerPage;

    return sortedThreats.slice(startIndex, startIndex + rowsPerPage);
  }, [sortedThreats, currentPage]);

  /*
    |--------------------------------------------------------------------------
    | RESET TO PAGE 1
    |--------------------------------------------------------------------------
    */

  useEffect(() => {
    setCurrentPage(1);
  }, [search, severity, kevOnly, sortColumn, sortDirection]);

  /*
    |--------------------------------------------------------------------------
    | SORT HANDLER
    |--------------------------------------------------------------------------
    */

  function handleSort(column: string) {
    if (sortColumn === column) {
      setSortDirection((previous) => (previous === "asc" ? "desc" : "asc"));
    } else {
      setSortColumn(column);

      setSortDirection("desc");
    }
  }

  function handleReset() {
    setSearch("");
    setSeverity("ALL");
    setKevOnly(false);

    // Reset sorting to default
    setSortColumn("severity");
    setSortDirection("desc");

    // Reset pagination
    setCurrentPage(1);
  }

  /*
    |--------------------------------------------------------------------------
    | LOADING
    |--------------------------------------------------------------------------
    */

  if (loading) {
    return <div className="p-6">Loading threat intelligence...</div>;
  }

  /*
    |--------------------------------------------------------------------------
    | ERROR
    |--------------------------------------------------------------------------
    */

  if (errorType) {
    return (
      <AppErrorState
        type={errorType}
        onRetry={() => {
          window.location.reload();
        }}
      />
    );
  }

  /*
    |--------------------------------------------------------------------------
    | PAGE
    |--------------------------------------------------------------------------
    */

  return (
    <div className="relative h-[calc(100vh-4rem)] overflow-hidden">
      {/* Main Threat Intelligence Area */}

      <main className="h-full min-w-0 overflow-hidden p-6">
        <div className="mb-6">
          <h1 className="text-3xl font-bold">Threat Intelligence</h1>

          <p className="text-muted-foreground">
            Monitor vulnerabilities, exploitability, and affected technologies.
          </p>
        </div>

        {/* Filters */}

        <div className="mb-4">
          <ThreatFilters
            search={search}
            severity={severity}
            onSearchChange={setSearch}
            onSeverityChange={(value) => setSeverity(value ?? "ALL")}
            kevOnly={kevOnly}
            onKevChange={setKevOnly}
            onReset={handleReset}
          />
        </div>

        {/* Table */}

        <div className="h-[calc(100%-140px)] overflow-hidden rounded-lg border">
          <ThreatTable
            threats={paginatedThreats}
            onSelect={setSelectedThreat}
            sortColumn={sortColumn}
            sortDirection={sortDirection}
            onSort={handleSort}
            currentPage={currentPage}
            totalPages={totalPages}
            onPageChange={setCurrentPage}
            totalThreats={sortedThreats.length}
            rowsPerPage={rowsPerPage}
          />
        </div>
      </main>

      {/* Foreground Overlay */}

      {selectedThreat && (
        <div className="absolute inset-0 z-50 flex items-center justify-center">
          {/* Background overlay */}

          <div
            className="absolute inset-0 bg-black/50 backdrop-blur-sm"
            onClick={() => setSelectedThreat(null)}
          />

          {/* Detail panel */}

          <div className="relative z-10 h-[90%] w-[90%] max-w-5xl overflow-hidden rounded-xl border bg-background shadow-2xl">
            <ThreatDetailPanel
              threat={selectedThreat}
              onClose={() => setSelectedThreat(null)}
            />
          </div>
        </div>
      )}
    </div>
  );
}
