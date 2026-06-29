"use client";

import React from "react";
import { PageHeader } from "@/components/shared/typography";
import { AnimatedContainer, GlassPanel } from "@/components/shared/containers";
import { AIStatus } from "@/components/shared/status";
import { FileCheck, FileWarning, ArrowRight, TrendingUp } from "lucide-react";
import { useAppStore } from "@/lib/store";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { Badge } from "@/components/ui/badge";

export default function FinalShortlistPage() {
  const workspace = useAppStore(state => state.workspace);

  if (!workspace) {
    return (
      <div className="flex flex-col items-center justify-center h-[60vh] space-y-6 text-center">
        <FileWarning className="w-16 h-16 text-muted-foreground opacity-50" />
        <div className="space-y-2">
          <h2 className="text-2xl font-bold">No Active Workspace</h2>
          <p className="text-muted-foreground max-w-md mx-auto">
            You need to select a job description and run the ranking pipeline before viewing the shortlist.
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

  const candidates = workspace.candidates.sort((a, b) => b.final_score - a.final_score).slice(0, 10);

  return (
    <div className="space-y-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <PageHeader 
          title="Final Shortlist" 
          description="The top candidates ranked by the unified ensemble scoring system."
        />
        <AIStatus status="complete" className="mb-8 bg-primary/10 border border-primary/20 px-3 py-1.5 rounded-full" />
      </div>

      <AnimatedContainer delay={0.1}>
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="text-xs uppercase text-muted-foreground bg-muted/50 border-b border-border">
              <tr>
                <th className="px-6 py-4 font-medium">Rank</th>
                <th className="px-6 py-4 font-medium">Candidate</th>
                <th className="px-6 py-4 font-medium">Hybrid</th>
                <th className="px-6 py-4 font-medium">Recruiter</th>
                <th className="px-6 py-4 font-medium">Behavior</th>
                <th className="px-6 py-4 font-medium text-primary">Final Score</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border/50">
              {candidates.map((candidate) => (
                <tr key={candidate.candidate_id} className="hover:bg-muted/30 transition-colors">
                  <td className="px-6 py-4 font-medium text-primary">#{candidate.overall_rank}</td>
                  <td className="px-6 py-4 font-medium">{candidate.candidate_id}</td>
                  <td className="px-6 py-4 text-blue-500">{(candidate.hybrid_score * 100).toFixed(1)}</td>
                  <td className="px-6 py-4 text-purple-500">{(candidate.recruiter_score * 100).toFixed(1)}</td>
                  <td className="px-6 py-4 text-amber-500">{(candidate.behavior_score * 100).toFixed(1)}</td>
                  <td className="px-6 py-4 font-bold text-emerald-500">{(candidate.final_score * 100).toFixed(1)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </AnimatedContainer>
    </div>
  );
}
