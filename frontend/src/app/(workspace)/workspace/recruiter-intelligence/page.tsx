"use client";

import React from "react";
import { PageHeader } from "@/components/shared/typography";
import { AnimatedContainer, GlassPanel } from "@/components/shared/containers";
import { AIStatus } from "@/components/shared/status";
import { EmptyState } from "@/components/shared/states";
import { BrainCircuit } from "lucide-react";

export default function RecruiterIntelligencePage() {
  return (
    <div className="space-y-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <PageHeader 
          title="Recruiter Intelligence" 
          description="Applying hard rules, domain heuristics, and tiering logic."
        />
        <AIStatus status="idle" className="mb-8 bg-muted/50 border border-border px-3 py-1.5 rounded-full" />
      </div>

      <AnimatedContainer delay={0.1}>
        <EmptyState 
          icon={BrainCircuit}
          title="Awaiting Module Activation" 
          description="The Recruiter Intelligence logic engine is currently waiting for the upstream Hybrid Retrieval fusion scores to finalize." 
        />
      </AnimatedContainer>
    </div>
  );
}
