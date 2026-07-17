"use client";

import {
  WifiOff,
  ServerCrash,
  RefreshCw,
  AlertTriangle,
  Clock3,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

interface Props {
  type: "network" | "timeout" | "backend" | "api" | "unknown";

  onRetry?: () => void;
}

const errorConfig = {
  network: {
    icon: WifiOff,
    title: "No Internet Connection",
    description:
      "Your device appears to be offline. Please check your internet connection and try again.",
  },

  timeout: {
    icon: Clock3,
    title: "Request Timed Out",
    description:
      "The request took too long to complete. The backend may be slow or temporarily unavailable.",
  },

  backend: {
    icon: ServerCrash,
    title: "Security Backend Unavailable",
    description:
      "NeosecAI could not connect to the security backend. Please check that the API service is running and accessible.",
  },

  api: {
    icon: AlertTriangle,
    title: "API Error",
    description:
      "The backend returned an unexpected error while processing your request.",
  },

  unknown: {
    icon: AlertTriangle,
    title: "Something Went Wrong",
    description: "An unexpected error occurred while loading this page.",
  },
};

export default function AppErrorState({ type, onRetry }: Props) {
  const config = errorConfig[type];

  const Icon = config.icon;

  return (
    <div className="flex min-h-[60vh] items-center justify-center p-6">
      <Card className="w-full max-w-md text-center shadow-sm">
        <CardHeader className="items-center">
          <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-muted">
            <Icon className="h-7 w-7 text-muted-foreground" />
          </div>

          <CardTitle className="text-xl">{config.title}</CardTitle>

          <CardDescription className="mt-2">
            {config.description}
          </CardDescription>
        </CardHeader>

        <CardContent>
          {onRetry && (
            <Button onClick={onRetry} className="gap-2">
              <RefreshCw className="h-4 w-4" />
              Try Again
            </Button>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
