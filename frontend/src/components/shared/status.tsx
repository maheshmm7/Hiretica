import React from "react";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { Sparkles, Activity, CheckCircle2, AlertCircle, Clock } from "lucide-react";

export function StatusBadge({ status, label }: { status: "success" | "warning" | "error" | "info" | "neutral"; label: string }) {
  const variants = {
    success: "bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 hover:bg-emerald-500/25 border-emerald-500/20",
    warning: "bg-amber-500/15 text-amber-600 dark:text-amber-400 hover:bg-amber-500/25 border-amber-500/20",
    error: "bg-rose-500/15 text-rose-600 dark:text-rose-400 hover:bg-rose-500/25 border-rose-500/20",
    info: "bg-blue-500/15 text-blue-600 dark:text-blue-400 hover:bg-blue-500/25 border-blue-500/20",
    neutral: "bg-muted text-muted-foreground hover:bg-muted/80 border-border"
  };

  return (
    <Badge variant="outline" className={cn("font-medium transition-colors", variants[status])}>
      {label}
    </Badge>
  );
}

export function AIStatus({ status = "idle", className }: { status?: "idle" | "processing" | "complete" | "error"; className?: string }) {
  const config = {
    idle: { icon: Clock, text: "Ready", color: "text-muted-foreground" },
    processing: { icon: Activity, text: "AI Processing", color: "text-blue-500 animate-pulse" },
    complete: { icon: Sparkles, text: "AI Generated", color: "text-emerald-500" },
    error: { icon: AlertCircle, text: "Failed", color: "text-rose-500" }
  };
  
  const { icon: Icon, text, color } = config[status];

  return (
    <div className={cn("flex items-center gap-1.5 text-xs font-medium", color, className)}>
      <Icon className="h-3.5 w-3.5" />
      <span>{text}</span>
    </div>
  );
}
