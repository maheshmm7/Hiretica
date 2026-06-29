import React from "react";
import { cn } from "@/lib/utils";
import { FileSearch, Loader2 } from "lucide-react";

export function EmptyState({ title, description, icon: Icon = FileSearch, action, className }: { title: string; description: string; icon?: React.ElementType; action?: React.ReactNode; className?: string }) {
  return (
    <div className={cn("flex flex-col items-center justify-center p-12 text-center rounded-xl border border-dashed border-border bg-background/30 backdrop-blur-sm", className)}>
      <div className="flex h-16 w-16 items-center justify-center rounded-full bg-muted/50 mb-4">
        <Icon className="h-8 w-8 text-muted-foreground" />
      </div>
      <h3 className="text-lg font-semibold">{title}</h3>
      <p className="text-sm text-muted-foreground mt-2 max-w-sm">{description}</p>
      {action && <div className="mt-6">{action}</div>}
    </div>
  );
}

export function LoadingState({ message = "Loading...", className }: { message?: string; className?: string }) {
  return (
    <div className={cn("flex flex-col items-center justify-center p-12 min-h-[400px]", className)}>
      <Loader2 className="h-8 w-8 animate-spin text-primary mb-4" />
      <p className="text-sm text-muted-foreground animate-pulse">{message}</p>
    </div>
  );
}
