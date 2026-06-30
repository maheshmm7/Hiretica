import React from "react";
import { cn } from "@/lib/utils";
import { Sparkles, Activity, AlertCircle, Clock } from "lucide-react";

const AI_STATUS_CONFIG = {
  idle: { icon: Clock, text: "Ready", color: "text-muted-foreground" },
  processing: { icon: Activity, text: "AI Processing", color: "text-blue-500 animate-pulse" },
  complete: { icon: Sparkles, text: "AI Generated", color: "text-emerald-500" },
  error: { icon: AlertCircle, text: "Failed", color: "text-rose-500" }
};

export function AIStatus({ status = "idle", className }: { status?: "idle" | "processing" | "complete" | "error"; className?: string }) {

  
  const { icon: Icon, text, color } = AI_STATUS_CONFIG[status];

  return (
    <div className={cn("flex items-center gap-1.5 text-xs font-medium", color, className)}>
      <Icon className="h-3.5 w-3.5" />
      <span>{text}</span>
    </div>
  );
}
