"use client";

import React from "react";
import { PageHeader } from "@/components/shared/typography";
import { AnimatedContainer } from "@/components/shared/containers";
import { AIStatus } from "@/components/shared/status";
import { EmptyState } from "@/components/shared/states";
import { Lightbulb } from "lucide-react";

export default function BehaviorIntelligencePage() {
  return (
    <div className="space-y-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <PageHeader 
          title="Behavior Intelligence" 
          description="Analyzing Redrob platform engagement, velocity, and intent signals."
        />
        <AIStatus status="idle" className="mb-8 bg-muted/50 border border-border px-3 py-1.5 rounded-full" />
      </div>

      <AnimatedContainer delay={0.1}>
        <EmptyState 
          icon={Lightbulb}
          title="Awaiting Module Activation" 
          description="Behavioral analysis is queued. It requires the shortlisting pipeline to complete before calculating conversion intent." 
        />
      </AnimatedContainer>
    </div>
  );
}
