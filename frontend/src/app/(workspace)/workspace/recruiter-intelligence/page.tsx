"use client";

import React from "react";
import { PageHeader } from "@/components/shared/typography";
import { AnimatedContainer, GlassPanel } from "@/components/shared/containers";
import { AIStatus } from "@/components/shared/status";
import { EmptyState } from "@/components/shared/states";
import { BrainCircuit, FileWarning, ArrowRight, TrendingUp } from "lucide-react";
import { useAppStore } from "@/lib/store";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";

export default function RecruiterIntelligencePage() {
  const workspace = useAppStore(state => state.workspace);

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

  const chartData = Object.entries(workspace.chart_data.recruiter_distribution).map(([key, value]) => ({
    name: key,
    count: value
  }));

  const candidates = workspace.candidates.sort((a, b) => b.recruiter_score - a.recruiter_score);

  return (
    <div className="space-y-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <PageHeader 
          title="Recruiter Intelligence" 
          description="Applying hard rules, domain heuristics, and tiering logic."
        />
        <AIStatus status="complete" className="mb-8 bg-purple-500/10 border border-purple-500/20 px-3 py-1.5 rounded-full" />
      </div>

      <AnimatedContainer delay={0.1} className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <GlassPanel className="p-6">
          <h3 className="text-lg font-bold mb-4 flex items-center gap-2"><TrendingUp className="w-5 h-5 text-purple-500" /> Score Distribution</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                <XAxis dataKey="name" stroke="#888" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#888" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  cursor={{fill: 'rgba(255,255,255,0.05)'}}
                  contentStyle={{backgroundColor: '#111', borderColor: '#333', borderRadius: '8px'}}
                />
                <Bar dataKey="count" fill="#a855f7" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </GlassPanel>

        <GlassPanel className="p-6">
          <h3 className="text-lg font-bold mb-4">Top Recruiter Matches</h3>
          <div className="space-y-4">
            {candidates.slice(0, 5).map(candidate => (
              <div key={candidate.candidate_id} className="flex items-center justify-between p-3 rounded-lg bg-muted/30 border border-border/50">
                <div className="font-medium">{candidate.candidate_id}</div>
                <div className="flex items-center gap-4">
                  <div className="text-sm text-muted-foreground">Recruiter Score</div>
                  <div className="font-bold text-purple-500">{(candidate.recruiter_score * 100).toFixed(1)}</div>
                </div>
              </div>
            ))}
          </div>
        </GlassPanel>
      </AnimatedContainer>
    </div>
  );
}
