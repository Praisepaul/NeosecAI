"use client";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

import { Button } from "@/components/ui/button";

import {
  ChevronDown,
  ChevronUp,
  ChevronsUpDown,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";

import { ThreatSummary } from "@/types/threat";

interface Props {
  threats: ThreatSummary[];

  onSelect: (threat: ThreatSummary) => void;

  sortColumn: string;

  sortDirection: "asc" | "desc";

  onSort: (column: string) => void;

  currentPage: number;

  totalPages: number;

  onPageChange: (page: number) => void;

  totalThreats: number;

  rowsPerPage: number;
}

function SortIcon({
  column,
  sortColumn,
  sortDirection,
}: {
  column: string;
  sortColumn: string;
  sortDirection: "asc" | "desc";
}) {
  if (column !== sortColumn) {
    return <ChevronsUpDown className="ml-1 h-4 w-4 opacity-40" />;
  }

  return sortDirection === "asc" ? (
    <ChevronUp className="ml-1 h-4 w-4" />
  ) : (
    <ChevronDown className="ml-1 h-4 w-4" />
  );
}

function SortableHeader({
  column,
  children,
  sortColumn,
  sortDirection,
  onSort,
}: {
  column: string;
  children: React.ReactNode;
  sortColumn: string;
  sortDirection: "asc" | "desc";
  onSort: (column: string) => void;
}) {
  return (
    <TableHead>
      <button
        onClick={() => onSort(column)}
        className="
                    flex
                    items-center
                    whitespace-nowrap
                    font-semibold
                    hover:text-primary
                "
      >
        {children}

        <SortIcon
          column={column}
          sortColumn={sortColumn}
          sortDirection={sortDirection}
        />
      </button>
    </TableHead>
  );
}

function getPageNumbers(
  currentPage: number,
  totalPages: number,
): (number | "...")[] {
  if (totalPages <= 5) {
    return Array.from({ length: totalPages }, (_, index) => index + 1);
  }

  if (currentPage <= 3) {
    return [1, 2, 3, 4, "...", totalPages];
  }

  if (currentPage >= totalPages - 2) {
    return [
      1,
      "...",
      totalPages - 3,
      totalPages - 2,
      totalPages - 1,
      totalPages,
    ];
  }

  return [
    1,
    "...",
    currentPage - 1,
    currentPage,
    currentPage + 1,
    "...",
    totalPages,
  ];
}

export default function ThreatTable({
  threats,
  onSelect,

  sortColumn,
  sortDirection,
  onSort,

  currentPage,
  totalPages,
  onPageChange,

  totalThreats,
  rowsPerPage,
}: Props) {
  const firstRow = totalThreats === 0 ? 0 : (currentPage - 1) * rowsPerPage + 1;

  const lastRow = Math.min(currentPage * rowsPerPage, totalThreats);

  return (
    <div className="flex h-full flex-col">
      {/* TABLE */}

      <div className="min-h-0 flex-1 overflow-y-auto thin-scrollbar">
        <Table>
          <TableHeader
            className="
                            sticky
                            top-0
                            z-10
                            bg-background
                        "
          >
            <TableRow>
              <SortableHeader
                column="cve"
                sortColumn={sortColumn}
                sortDirection={sortDirection}
                onSort={onSort}
              >
                CVE
              </SortableHeader>

              <SortableHeader
                column="title"
                sortColumn={sortColumn}
                sortDirection={sortDirection}
                onSort={onSort}
              >
                Title
              </SortableHeader>

              <SortableHeader
                column="severity"
                sortColumn={sortColumn}
                sortDirection={sortDirection}
                onSort={onSort}
              >
                Severity
              </SortableHeader>

              <SortableHeader
                column="cvss"
                sortColumn={sortColumn}
                sortDirection={sortDirection}
                onSort={onSort}
              >
                CVSS
              </SortableHeader>

              <SortableHeader
                column="risk"
                sortColumn={sortColumn}
                sortDirection={sortDirection}
                onSort={onSort}
              >
                Risk
              </SortableHeader>

              <SortableHeader
                column="epss"
                sortColumn={sortColumn}
                sortDirection={sortDirection}
                onSort={onSort}
              >
                EPSS
              </SortableHeader>

              <SortableHeader
                column="assets"
                sortColumn={sortColumn}
                sortDirection={sortDirection}
                onSort={onSort}
              >
                Assets
              </SortableHeader>

              <SortableHeader
                column="published"
                sortColumn={sortColumn}
                sortDirection={sortDirection}
                onSort={onSort}
              >
                Published
              </SortableHeader>
            </TableRow>
          </TableHeader>

          <TableBody>
            {threats.length === 0 ? (
              <TableRow>
                <TableCell
                  colSpan={8}
                  className="
                                        h-32
                                        text-center
                                        text-muted-foreground
                                    "
                >
                  No threats found
                </TableCell>
              </TableRow>
            ) : (
              threats.map((threat) => (
                <TableRow
                  key={threat.cve}
                  className="
                                            cursor-pointer
                                            hover:bg-muted/50
                                        "
                  onClick={() => onSelect(threat)}
                >
                  <TableCell
                    className="
                                                font-medium
                                                whitespace-nowrap
                                            "
                  >
                    {threat.cve}
                  </TableCell>

                  <TableCell
                    className="
                                                max-w-[400px]
                                                truncate
                                            "
                  >
                    {threat.title || "N/A"}
                  </TableCell>

                  <TableCell>
                    <span
                      className={`
                                                    rounded-full
                                                    px-2
                                                    py-1
                                                    text-xs
                                                    font-medium

                                                    ${
                                                      threat.cvss?.severity ===
                                                      "CRITICAL"
                                                        ? "bg-red-500/15 text-red-500"
                                                        : threat.cvss
                                                              ?.severity ===
                                                            "HIGH"
                                                          ? "bg-orange-500/15 text-orange-500"
                                                          : threat.cvss
                                                                ?.severity ===
                                                              "MEDIUM"
                                                            ? "bg-yellow-500/15 text-yellow-600"
                                                            : "bg-green-500/15 text-green-600"
                                                    }
                                                `}
                    >
                      {threat.cvss?.severity || "UNKNOWN"}
                    </span>
                  </TableCell>

                  <TableCell>{threat.cvss?.score ?? "N/A"}</TableCell>

                  <TableCell>{threat.risk_score}</TableCell>

                  <TableCell>
                    {threat.epss?.score != null
                      ? (threat.epss.score * 100).toFixed(2) + "%"
                      : "N/A"}
                  </TableCell>

                  <TableCell>{threat.matched_assets?.length || 0}</TableCell>

                  <TableCell
                    className="
                                                whitespace-nowrap
                                            "
                  >
                    {threat.published
                      ? new Date(threat.published).toLocaleDateString()
                      : "N/A"}
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>

      {/* PAGINATION */}

      <div
        className="
    flex
    flex-col
    gap-1
    border-t
    bg-background
    px-3
    py-1.5

    sm:flex-row
    sm:items-center
    sm:justify-between
  "
      >
        {/* Result count */}

        <div
          className="
      text-xs
      text-muted-foreground
    "
        >
          Showing{" "}
          <span className="font-medium text-foreground">{firstRow}</span> to{" "}
          <span className="font-medium text-foreground">{lastRow}</span> of{" "}
          <span className="font-medium text-foreground">{totalThreats}</span>{" "}
          threats
        </div>

        {/* Pagination controls */}

        <div
          className="
      flex
      items-center
      gap-0.5
      cursor-pointer
    "
        >
          {/* Previous */}

          <Button
            variant="outline"
            size="sm"
            disabled={currentPage === 1}
            onClick={() => onPageChange(currentPage - 1)}
            className="
        h-7
        px-2
        text-xs
        mr-1
        cursor-pointer
      "
          >
            <ChevronLeft className="mr-0.5 h-3 w-3" />
            Previous
          </Button>

          {/* Page numbers */}

          <div className="flex items-center gap-0.5">
            {getPageNumbers(currentPage, totalPages).map((page, index) => {
              if (page === "...") {
                return (
                  <span
                    key={`ellipsis-${index}`}
                    className="
                flex
                h-7
                w-6
                items-center
                justify-center
                text-xs
                text-muted-foreground
              "
                  >
                    ...
                  </span>
                );
              }

              return (
                <button
                  key={page}
                  onClick={() => onPageChange(page)}
                  className={`
              flex
              h-7
              min-w-7
              items-center
              justify-center
              rounded-md
              border
              px-1.5
              text-xs
              transition-colors
              cursor-pointer
              ${
                currentPage === page
                  ? "border-primary bg-primary text-primary-foreground"
                  : "border-border bg-background hover:bg-muted"
              }
            `}
                >
                  {page}
                </button>
              );
            })}
          </div>

          {/* Next */}

          <Button
            variant="outline"
            size="sm"
            disabled={currentPage >= totalPages}
            onClick={() => onPageChange(currentPage + 1)}
            className="
        h-7
        px-2
        text-xs
        ml-1
        cursor-pointer
      "
          >
            Next
            <ChevronRight className="ml-0.5 h-3 w-3" />
          </Button>
        </div>
      </div>
    </div>
  );
}
