"use client";

import React from "react";
import { PageHeader } from "@/components/shared/typography";
import { AnimatedContainer, GlassPanel } from "@/components/shared/containers";
import { AIStatus } from "@/components/shared/status";
import {  FileWarning, ArrowRight, TrendingUp } from "lucide-react";
import { useAppStore } from "@/lib/store";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import dynamic from "next/dynamic";

const GenericBarChart = dynamic(() => import("@/components/charts/generic-bar-chart"), { ssr: false });

export default function BehaviorIntelligencePage() {
  const workspace = useAppStore(state => state.workspace);
  const selectedCandidate = useAppStore(state => state.selectedCandidate);
  const setSelectedCandidate = useAppStore(state => state.setSelectedCandidate);

  if (!workspace) {
    return (
      <div className="flex flex-col items-center justify-center h-[60vh] space-y-6 text-center">
        <FileWarning className="w-16 h-16 text-muted-foreground opacity-50" />
        <div className="space-y-2">
          <h2 className="text-2xl font-bold">No Active Workspace</h2>
          <p className="text-muted-foreground max-w-md mx-auto">
            You need to select a job description and run the ranking pipeline before viewing intelligence.
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

  const chartData = Object.entries(workspace.chart_data.behavior_distribution).map(([key, value]) => ({
    name: key,
    count: value
  }));

  const candidates = workspace.candidates.toSorted((a, b) => b.behavior_score - a.behavior_score);

  return (
    <div className="space-y-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <PageHeader 
          title="Behavior Intelligence" 
          description="Analyzing Redrob platform engagement, velocity, and intent signals."
        />
        <AIStatus status="complete" className="mb-8 bg-amber-500/10 border border-amber-500/20 px-3 py-1.5 rounded-full" />
      </div>

      <AnimatedContainer delay={0.1} className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <GlassPanel className="p-6">
          <h3 className="text-lg font-bold mb-4 flex items-center gap-2"><TrendingUp className="w-5 h-5 text-amber-500" /> Behavior Score Distribution</h3>
          <div className="h-64">
            <GenericBarChart data={chartData} color="#f59e0b" />
          </div>
        </GlassPanel>

        <GlassPanel className="p-6">
          <h3 className="text-lg font-bold mb-4">Top Behavior Matches</h3>
          <div className="space-y-4">
            {candidates.slice(0, 5).map(candidate => (
              <button 
                type="button"
                key={candidate.candidate_id} 
                className={`w-full flex items-center justify-between p-3 rounded-lg border transition-colors cursor-pointer ${selectedCandidate === candidate.candidate_id ? 'bg-amber-500/10 border-amber-500/50' : 'bg-muted/30 border-border/50 hover:border-amber-500/30'}`}
                onClick={() => setSelectedCandidate(candidate.candidate_id)}
              >
                <div className="font-medium">{candidate.candidate_id}</div>
                <div className="flex items-center gap-4">
                  <div className="text-sm text-muted-foreground">Behavior Score</div>
                  <div className="font-bold text-amber-500">{(candidate.behavior_score * 100).toFixed(1)}</div>
                </div>
              </button>
            ))}
          </div>
        </GlassPanel>
      </AnimatedContainer>
    </div>
  );
}
