"use client";

import React from "react";
import { PageHeader } from "@/components/shared/typography";
import { AnimatedContainer, GlassPanel } from "@/components/shared/containers";
import { AIStatus } from "@/components/shared/status";
import { ShieldCheck, FileWarning, ArrowRight } from "lucide-react";
import { useAppStore } from "@/lib/store";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { Badge } from "@/components/ui/badge";

export default function ExplainabilityPage() {
  const workspace = useAppStore(state => state.workspace);

  if (!workspace) {
    return (
      <div className="flex flex-col items-center justify-center h-[60vh] space-y-6 text-center">
        <FileWarning className="w-16 h-16 text-muted-foreground opacity-50" />
        <div className="space-y-2">
          <h2 className="text-2xl font-bold">No Active Workspace</h2>
          <p className="text-muted-foreground max-w-md mx-auto">
            You need to select a job description and run the ranking pipeline before viewing explainability.
          </p>
        </div>
        <Link href="/workspace/job-understanding">
          <Button className="gap-2">
            Select Job Description <ArrowRight className="w-4 h-4" />
          </Button>
        </Link>
      </div>
    );
  }

  const candidates = workspace.candidates.slice(0, 50);

  return (
    <div className="space-y-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <PageHeader 
          title="Explainability" 
          description="Transparent AI reasoning and deterministic feature attribution."
        />
        <AIStatus status="complete" className="mb-8 bg-emerald-500/10 border border-emerald-500/20 px-3 py-1.5 rounded-full" />
      </div>

      <AnimatedContainer delay={0.1} className="grid grid-cols-1 gap-6">
        {candidates.map(candidate => (
          <GlassPanel key={candidate.candidate_id} className="p-6">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h3 className="text-lg font-bold">{candidate.candidate_id}</h3>
                <p className="text-sm font-medium text-foreground/80 mt-1 flex items-center gap-2">
                  <Badge variant="outline">Rank #{candidate.overall_rank}</Badge>
                </p>
              </div>
              <div className="text-right">
                <div className="text-xs text-muted-foreground mb-1">Final Score</div>
                <div className="text-2xl font-bold text-emerald-500">{(candidate.final_score * 100).toFixed(1)}</div>
              </div>
            </div>

            <div className="bg-muted/30 p-4 rounded-lg border border-border/50 mb-6 relative overflow-hidden">
              <div className="absolute top-0 left-0 w-1 h-full bg-emerald-500" />
              <div className="text-sm font-semibold uppercase tracking-wider text-muted-foreground mb-2 flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-emerald-500" /> AI Rationale
              </div>
              <p className="text-sm leading-relaxed">{candidate.reasoning}</p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-3">
                <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Positive Evidence</div>
                <div className="flex flex-col gap-2">
                  {candidate.positive_factors.map((factor, i) => (
                    <div key={i} className="text-sm flex items-start gap-2">
                      <span className="text-emerald-500 font-bold">+</span> {factor}
                    </div>
                  ))}
                </div>
              </div>
              
              <div className="space-y-3">
                <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Risk Factors</div>
                <div className="flex flex-col gap-2">
                  {candidate.negative_factors.map((factor, i) => (
                    <div key={i} className="text-sm flex items-start gap-2">
                      <span className="text-amber-500 font-bold">-</span> {factor}
                    </div>
                  ))}
                  {candidate.negative_factors.length === 0 && (
                    <div className="text-sm text-muted-foreground italic">None detected.</div>
                  )}
                </div>
              </div>
            </div>
          </GlassPanel>
        ))}
      </AnimatedContainer>
    </div>
  );
}
