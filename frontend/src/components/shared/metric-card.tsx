import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { LucideIcon } from "lucide-react";

interface MetricCardProps {
  title: string;
  value: string | number;
  description?: string;
  icon?: LucideIcon;
  trend?: { value: number; label: string; positive?: boolean };
  className?: string;
}

export function MetricCard({ title, value, description, icon: Icon, trend, className }: MetricCardProps) {
  return (
    <Card className={cn("overflow-hidden border-border/50 bg-background/50 backdrop-blur-sm", className)}>
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">{title}</CardTitle>
        {Icon && <Icon className="h-4 w-4 text-muted-foreground" />}
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        {(description || trend) && (
          <div className="mt-1 flex items-center text-xs">
            {trend && (
              <span className={cn("mr-2 font-medium", trend.positive ? "text-emerald-500" : "text-rose-500")}>
                {trend.positive ? "+" : "-"}{Math.abs(trend.value)}%
              </span>
            )}
            <span className="text-muted-foreground">{description || trend?.label}</span>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
