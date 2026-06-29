"use client";

import React from "react";
import { PageHeader } from "@/components/shared/typography";
import { AnimatedContainer, GlassPanel } from "@/components/shared/containers";
import { AIStatus } from "@/components/shared/status";
import { EmptyState } from "@/components/shared/states";
import { FileCheck } from "lucide-react";

export default function FinalShortlistPage() {
  return (
    <div className="space-y-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <PageHeader 
          title="Final Shortlist" 
          description="The top candidates ranked by the unified ensemble scoring system."
        />
        <AIStatus status="idle" className="mb-8 bg-muted/50 border border-border px-3 py-1.5 rounded-full" />
      </div>

      <AnimatedContainer delay={0.1}>
        <EmptyState 
          icon={FileCheck}
          title="Awaiting Pipeline Completion" 
          description="The final shortlist will populate here once the entire processing pipeline completes and ensemble weights are applied." 
        />
      </AnimatedContainer>
    </div>
  );
}
