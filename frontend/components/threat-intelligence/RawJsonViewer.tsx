"use client";

import { useState } from "react";
import { Check, Copy, Download, Maximize2, Minimize2 } from "lucide-react";

import { Button } from "@/components/ui/button";

import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";

interface RawJsonViewerProps {
  data: unknown;
  fileName?: string;
}

export default function RawJsonViewer({
  data,
  fileName = "raw-data.json",
}: RawJsonViewerProps) {
  const [copied, setCopied] = useState(false);
  const [expanded, setExpanded] = useState(false);

  const json = JSON.stringify(data, null, 2);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(json);

    setCopied(true);

    setTimeout(() => {
      setCopied(false);
    }, 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([json], {
      type: "application/json",
    });

    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");

    link.href = url;
    link.download = fileName;

    document.body.appendChild(link);
    link.click();

    document.body.removeChild(link);

    URL.revokeObjectURL(url);
  };

  return (
    <div
      className={
        expanded
          ? "fixed inset-0 z-50 flex flex-col bg-background p-6"
          : "relative"
      }
    >
      {/* TOOLBAR */}

      <div className="flex items-center justify-between border-b bg-muted/30 px-3 py-2">
        <span className="text-xs font-medium text-muted-foreground">
          Raw JSON
        </span>

        <div className="flex items-center gap-1">
          {/* COPY */}

          <Button
            variant="ghost"
            size="sm"
            onClick={handleCopy}
            className="h-8 gap-2 text-xs cursor-pointer"
          >
            {copied ? (
              <>
                <Check className="h-3.5 w-3.5" />
                Copied
              </>
            ) : (
              <>
                <Copy className="h-3.5 w-3.5" />
                Copy
              </>
            )}
          </Button>

          {/* DOWNLOAD */}

          <Button
            variant="ghost"
            size="sm"
            onClick={handleDownload}
            className="h-8 gap-2 text-xs cursor-pointer"
          >
            <Download className="h-3.5 w-3.5" />
            Download
          </Button>

          {/* EXPAND */}

          <Button
            variant="ghost"
            size="icon"
            onClick={() => setExpanded(!expanded)}
            className="h-8 w-8 cursor-pointer"
          >
            {expanded ? (
              <Minimize2 className="h-4 w-4" />
            ) : (
              <Maximize2 className="h-4 w-4" />
            )}
          </Button>
        </div>
      </div>

      {/* JSON */}

      <div
        className={
          expanded
            ? "min-h-0 flex-1 overflow-auto"
            : "max-h-[600px] overflow-auto"
        }
      >
        <SyntaxHighlighter
          language="json"
          style={vscDarkPlus}
          customStyle={{
            margin: 0,
            borderRadius: 0,
            fontSize: "12px",
            lineHeight: "1.6",
          }}
          wrapLongLines
        >
          {json}
        </SyntaxHighlighter>
      </div>
    </div>
  );
}
