"use client";

import React from "react";
import { PageHeader } from "@/components/shared/typography";
import { AnimatedContainer } from "@/components/shared/containers";
import { AIStatus } from "@/components/shared/status";
import { EmptyState } from "@/components/shared/states";
import { ShieldCheck } from "lucide-react";

export default function ExplainabilityPage() {
  return (
    <div className="space-y-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <PageHeader 
          title="Explainability" 
          description="Transparent AI reasoning and deterministic feature attribution."
        />
        <AIStatus status="idle" className="mb-8 bg-muted/50 border border-border px-3 py-1.5 rounded-full" />
      </div>

      <AnimatedContainer delay={0.1}>
        <EmptyState 
          icon={ShieldCheck}
          title="No rationales generated yet" 
          description="Natural language rationales will be synthesized for the top ranked candidates once the final scoring ensemble executes." 
        />
      </AnimatedContainer>
    </div>
  );
}
