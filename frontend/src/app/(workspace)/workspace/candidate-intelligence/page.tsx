"use client";

import React from "react";
import { PageHeader } from "@/components/shared/typography";
import { AnimatedContainer, GlassPanel } from "@/components/shared/containers";
import { mockCandidates } from "@/lib/mock/candidates";
import { Badge } from "@/components/ui/badge";
import { Search, MapPin, Briefcase, FileWarning, ArrowRight } from "lucide-react";
import { Input } from "@/components/ui/input";
import { useAppStore } from "@/lib/store";
import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function CandidateIntelligencePage() {
  const workspace = useAppStore(state => state.workspace);
  
  if (!workspace) {
    return (
      <div className="flex flex-col items-center justify-center h-[60vh] space-y-6 text-center">
        <FileWarning className="w-16 h-16 text-muted-foreground opacity-50" />
        <div className="space-y-2">
          <h2 className="text-2xl font-bold">No Active Workspace</h2>
          <p className="text-muted-foreground max-w-md mx-auto">
            You need to select a job description and run the ranking pipeline before exploring candidate intelligence.
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

  const candidates = workspace.candidates;

  return (
    <div className="space-y-8">
      <PageHeader 
        title="Candidate Intelligence" 
        description="Explore the global candidate pool and extracted semantic features."
      />

      <AnimatedContainer delay={0.1}>
        <div className="relative mb-8 max-w-xl">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
          <Input 
            placeholder="Search by name, role, or skill..." 
            className="pl-10 h-12 bg-background/50 backdrop-blur-sm border-border/50 focus-visible:ring-primary/20"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <div className="bg-background/50 p-4 rounded-xl border border-border/50">
            <div className="text-sm text-muted-foreground mb-1">Total Processed</div>
            <div className="text-2xl font-bold">{workspace.dashboard_metrics.total_candidates.toLocaleString()}</div>
          </div>
          <div className="bg-background/50 p-4 rounded-xl border border-border/50">
            <div className="text-sm text-muted-foreground mb-1">Avg AI Score</div>
            <div className="text-2xl font-bold text-emerald-500">{(workspace.dashboard_metrics.avg_score * 100).toFixed(1)}</div>
          </div>
          <div className="bg-background/50 p-4 rounded-xl border border-border/50">
            <div className="text-sm text-muted-foreground mb-1">Recruiter Avg</div>
            <div className="text-2xl font-bold text-blue-500">{workspace.dashboard_metrics.avg_recruiter.toFixed(1)}</div>
          </div>
          <div className="bg-background/50 p-4 rounded-xl border border-border/50">
            <div className="text-sm text-muted-foreground mb-1">Behavior Avg</div>
            <div className="text-2xl font-bold text-amber-500">{workspace.dashboard_metrics.avg_behavior.toFixed(1)}</div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {candidates.slice(0, 50).map((candidate, i) => (
            <GlassPanel key={candidate.candidate_id} className="p-6 hover:border-primary/20 transition-colors cursor-pointer group">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-lg font-bold group-hover:text-primary transition-colors">{candidate.candidate_id}</h3>
                  <p className="text-sm font-medium text-foreground/80 mt-1 flex items-center gap-2">
                    <Badge variant="outline">Rank #{candidate.overall_rank}</Badge>
                  </p>
                </div>
                <div className="text-right">
                  <div className="text-xs text-muted-foreground mb-1">Match Score</div>
                  <div className="text-2xl font-bold text-emerald-500">{(candidate.final_score * 100).toFixed(1)}</div>
                </div>
              </div>

              <div className="space-y-3 mb-6">
                <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Reasoning Overview</div>
                <p className="text-sm text-muted-foreground leading-relaxed line-clamp-3">
                  {candidate.reasoning}
                </p>
              </div>

              <div className="space-y-3">
                <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Factors</div>
                <div className="flex flex-wrap gap-2">
                  {candidate.positive_factors.slice(0, 3).map(factor => (
                    <Badge key={factor} variant="secondary" className="bg-emerald-500/10 text-emerald-500 hover:bg-emerald-500/20 border-emerald-500/20">
                      + {factor}
                    </Badge>
                  ))}
                  {candidate.negative_factors.slice(0, 2).map(factor => (
                    <Badge key={factor} variant="secondary" className="bg-amber-500/10 text-amber-500 hover:bg-amber-500/20 border-amber-500/20">
                      - {factor}
                    </Badge>
                  ))}
                </div>
              </div>
            </GlassPanel>
          ))}
        </div>
      </AnimatedContainer>
    </div>
  );
}
