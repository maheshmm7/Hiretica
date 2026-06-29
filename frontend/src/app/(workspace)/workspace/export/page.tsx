"use client";

import React from "react";
import { PageHeader } from "@/components/shared/typography";
import { AnimatedContainer, GlassPanel } from "@/components/shared/containers";
import { AIStatus } from "@/components/shared/status";
import { EmptyState } from "@/components/shared/states";
import { Download } from "lucide-react";

export default function ExportPage() {
  return (
    <div className="space-y-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <PageHeader 
          title="Export Submission" 
          description="Generate the final CSV artifact required for the hackathon submission."
        />
        <AIStatus status="idle" className="mb-8 bg-muted/50 border border-border px-3 py-1.5 rounded-full" />
      </div>

      <AnimatedContainer delay={0.1}>
        <EmptyState 
          icon={Download}
          title="Export Unavailable" 
          description="Awaiting the generation of the final shortlist before compiling the export artifact (submission.csv)." 
        />
      </AnimatedContainer>
    </div>
  );
}
