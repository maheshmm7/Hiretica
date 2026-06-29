"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { 
  Activity, Search, Users, Database, BrainCircuit, 
  Lightbulb, ShieldCheck, FileCheck, Download, Beaker
} from "lucide-react";

const NAV_ITEMS = [
  { name: "Mission Control", href: "/workspace/mission-control", icon: Activity },
  { name: "Job Understanding", href: "/workspace/job-understanding", icon: Search },
  { name: "Candidate Intelligence", href: "/workspace/candidate-intelligence", icon: Users },
  { name: "Hybrid Retrieval", href: "/workspace/hybrid-retrieval", icon: Database },
  { name: "Recruiter Intelligence", href: "/workspace/recruiter-intelligence", icon: BrainCircuit },
  { name: "Behavior Intelligence", href: "/workspace/behavior-intelligence", icon: Lightbulb },
  { name: "Explainability", href: "/workspace/explainability", icon: ShieldCheck },
  { name: "Final Shortlist", href: "/workspace/final-shortlist", icon: FileCheck },
  { name: "Export", href: "/workspace/export", icon: Download },
  { name: "Science", href: "/workspace/science", icon: Beaker },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 border-r border-border bg-background/50 backdrop-blur-xl hidden md:flex flex-col flex-shrink-0 h-screen sticky top-0">
      <div className="h-16 flex items-center px-6 border-b border-border">
        <Link href="/" className="flex items-center gap-2">
          <div className="w-6 h-6 rounded bg-primary text-primary-foreground flex items-center justify-center font-bold text-xs">
            H
          </div>
          <span className="font-bold text-lg tracking-tight">HIRETICA</span>
        </Link>
      </div>

      <div className="flex-1 overflow-y-auto py-6 px-3 scroll-area">
        <div className="space-y-1">
          {NAV_ITEMS.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex items-center gap-3 px-3 py-2.5 rounded-md text-sm font-medium transition-colors",
                  isActive 
                    ? "bg-primary/10 text-primary" 
                    : "text-muted-foreground hover:bg-muted hover:text-foreground"
                )}
              >
                <item.icon className={cn("w-4 h-4", isActive ? "text-primary" : "text-muted-foreground")} />
                {item.name}
              </Link>
            );
          })}
        </div>
      </div>
      
      <div className="p-4 border-t border-border mt-auto">
        <div className="bg-muted/50 rounded-lg p-3 text-xs flex flex-col gap-2">
          <div className="flex items-center justify-between">
            <span className="text-muted-foreground font-medium">System Status</span>
            <div className="flex items-center gap-1.5 text-emerald-500">
              <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              <span>Online</span>
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
}
